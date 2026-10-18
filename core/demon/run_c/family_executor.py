#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUN C family executor.

World-content-blind executable layer for the frozen RUN C family dictionary.
No event names or tested-world identifiers are accepted by the public handler
interface. The historical RULE_TYPE names are compiler-target opcodes; behavior
is driven by record fields.
"""
from dataclasses import dataclass, field
from typing import Any, Iterable

try:
    from ..demon_core import Record, GO, BLOCK, NEED
except ImportError:
    from demon_core import Record, GO, BLOCK, NEED


OPEN = "OPEN"


@dataclass
class HandlerResult:
    verdict: str = GO
    classification: str | None = None
    proposed_delta: list = field(default_factory=list)
    derived_records: list = field(default_factory=list)
    provenance_requirements: list = field(default_factory=list)
    opens: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)
    stops: list = field(default_factory=list)
    unchecked_dependencies: list = field(default_factory=list)
    details: dict = field(default_factory=dict)


class SchemaError(ValueError):
    pass


def current_records(net):
    return [
        r for r in net.records.values()
        if r.f("PREDICATE") is not None
        and r.status_log
        and r.status_log[-1].state == "CURRENT"
    ]


def current_matches(net, subject=None, predicate=None, object_=None):
    out = []
    for r in current_records(net):
        if subject is not None and r.f("SUBJECT") != subject:
            continue
        if predicate is not None and r.f("PREDICATE") != predicate:
            continue
        if object_ is not None and r.f("OBJECT") != object_:
            continue
        out.append(r)
    return out


def current_values(net, subject, predicate):
    return [r.f("OBJECT") for r in current_matches(net, subject, predicate)]


def nested_get(obj, path):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def rule_dict(rule):
    return rule.fields if hasattr(rule, "fields") else rule


def rule_addr(rule):
    if hasattr(rule, "addr"):
        return rule.addr
    return rule.get("addr")


def rule_type(rule):
    return rule_dict(rule).get("RULE_TYPE")


def network_rules(net, rtype=None):
    out = []
    for r in net.records.values():
        if r.f("TYPE") != "RULE":
            continue
        if not r.status_log or r.status_log[-1].state != "CURRENT":
            continue
        if rtype is None or r.f("RULE_TYPE") == rtype:
            out.append(r)
    return out


def resolve_paths(data, path):
    """Resolve dictionary paths with [] for list expansion."""
    parts = path.split(".")
    vals = [data]
    for part in parts:
        expand = part.endswith("[]")
        key = part[:-2] if expand else part
        nxt = []
        for val in vals:
            if not isinstance(val, dict) or key not in val:
                continue
            got = val[key]
            if expand:
                if isinstance(got, list):
                    nxt.extend(got)
            else:
                nxt.append(got)
        vals = nxt
    return vals


def dependency_predicates(rule, family_spec):
    data = rule_dict(rule)
    out = set()
    for path in family_spec.get("dependency_signature", []):
        for val in resolve_paths(data, path):
            if isinstance(val, str):
                out.add(val)
    return out


def dependency_match(rule, family_spec, incoming):
    return incoming.f("PREDICATE") in dependency_predicates(rule, family_spec)


def _path_present(data, path):
    """True when a dictionary path exists; [] expands any list element."""
    parts = path.split(".")
    vals = [data]
    for part in parts:
        expand = part.endswith("[]")
        key = part[:-2] if expand else part
        nxt = []
        for val in vals:
            if not isinstance(val, dict) or key not in val:
                continue
            got = val[key]
            if expand:
                if isinstance(got, list):
                    nxt.extend(got)
            else:
                nxt.append(got)
        if not nxt:
            return False
        vals = nxt
    return True


def schema_contract_errors(rule, family_spec):
    data = rule_dict(rule)
    return [
        path for path in family_spec.get("required_paths", family_spec.get("required_fields", []))
        if not _path_present(data, path)
    ]


def unchecked_marker(addr, dependency, reason):
    return Record(addr, {
        "TYPE": "CHECK_STATUS",
        "STATUS": "UNCHECKED",
        "DEPENDENCY": dependency,
        "REASON": reason,
    })


def _filter_subjects(net, filt, scope, other_side_subjects=None):
    if "predicate" in filt:
        target = scope if filt.get("target") == "scoped_node" else filt.get("target")
        return {
            r.f("SUBJECT")
            for r in current_matches(net, predicate=filt["predicate"], object_=target)
        }

    if "all" in filt:
        sets = []
        subtract_other = False
        for clause in filt["all"]:
            if "predicate" in clause:
                target = scope if clause.get("target") == "scoped_node" else clause.get("target")
                sets.append({
                    r.f("SUBJECT")
                    for r in current_matches(net, predicate=clause["predicate"], object_=target)
                })
            elif clause.get("relation") in (
                "other_links_than_left",
                "other_members_than_other_side",
            ):
                subtract_other = True
            else:
                raise SchemaError(f"unsupported filter clause: {clause!r}")
        subjects = set.intersection(*sets) if sets else set()
        if subtract_other:
            subjects -= set(other_side_subjects or ())
        return subjects

    raise SchemaError(f"unsupported link_filter: {filt!r}")


def _eval_expression(net, expr, scope, other_side_subjects=None):
    if "lookup" in expr:
        lk = expr["lookup"]
        subject = scope if lk.get("subject") == "scoped_node" else lk.get("subject")
        vals = current_values(net, subject, lk["predicate"])
        if len(vals) != 1 or not isinstance(vals[0], int):
            return {
                "complete": False,
                "value": None,
                "subjects": {subject},
                "records": current_matches(net, subject, lk["predicate"]),
                "missing_subjects": {subject} if not vals else set(),
                "value_predicate": lk["predicate"],
            }
        return {
            "complete": True,
            "value": vals[0],
            "subjects": {subject},
            "records": current_matches(net, subject, lk["predicate"]),
            "missing_subjects": set(),
            "value_predicate": lk["predicate"],
        }

    if expr.get("aggregate") != "sum":
        raise SchemaError(f"unsupported expression: {expr!r}")

    subjects = _filter_subjects(net, expr["link_filter"], scope, other_side_subjects)
    records = []
    missing = set()
    values = []
    pred = expr["value_predicate"]
    for subject in subjects:
        rs = current_matches(net, subject, pred)
        vals = [r.f("OBJECT") for r in rs]
        if len(vals) != 1 or not isinstance(vals[0], int):
            missing.add(subject)
            records.extend(rs)
            continue
        values.append(vals[0])
        records.extend(rs)

    return {
        "complete": not missing,
        "value": sum(values) if not missing else None,
        "known_sum": sum(values),
        "subjects": subjects,
        "records": records,
        "missing_subjects": missing,
        "value_predicate": pred,
    }


def _equality_sides(net, rule, scope):
    eq = rule_dict(rule)["balance"]["equality"]
    left = _eval_expression(net, eq["left"], scope)
    right = _eval_expression(net, eq["right"], scope, left["subjects"])
    if "all" in eq["left"].get("link_filter", {}):
        left = _eval_expression(net, eq["left"], scope, right["subjects"])
    return left, right


def _closure_rule_for(rule, net):
    conditions = rule_dict(rule).get("derivation", {}).get("conditions", [])
    for cond in conditions:
        cfg = cond.get("adjacent_link_set")
        if cfg and cfg.get("closure_declared_by"):
            return net.read(cfg["closure_declared_by"])
    return None


def _closed_members(closure_rule, scope):
    if closure_rule is None:
        return None
    data = rule_dict(closure_rule)
    if data.get("RULE_TYPE") != "EXPLICIT_CLOSED_RELATION_SET":
        return None
    if data.get("set_status") != "closed" or data.get("closure_scope") != scope:
        return None
    return set(data.get("exact_members", []))


def handle_exact_cardinality(rule, net, request):
    data = rule_dict(rule)
    pred = data["predicate"]
    subject = request.get("SUBJECT")
    op = request["OP"]
    if op == "VALIDATE_INCOMING":
        incoming = request["INCOMING"]
        if incoming.f("PREDICATE") != pred:
            return HandlerResult(details={"applicable": False})
        subject = incoming.f("SUBJECT")
        existing = current_values(net, subject, pred)
        candidate = existing + [incoming.f("OBJECT")]
        if len(candidate) > data["target_count"] or (
            data.get("target_distinctness") == "pairwise_distinct"
            and len(set(candidate)) != len(candidate)
        ):
            return HandlerResult(
                verdict=BLOCK,
                conflicts=[{"rule": rule_addr(rule), "subject": subject, "values": candidate}],
                details={"applicable": True},
            )
        return HandlerResult(details={"applicable": True, "observed": candidate})

    vals = current_values(net, subject, pred)
    distinct = len(vals) == len(set(vals))
    target = data["target_count"]
    if len(vals) > target or not distinct:
        return HandlerResult(
            verdict=BLOCK,
            conflicts=[{"rule": rule_addr(rule), "subject": subject, "values": vals}],
            details={"observed_count": len(vals), "target_count": target},
        )
    if len(vals) < target:
        return HandlerResult(
            verdict=OPEN,
            opens=[{"rule": rule_addr(rule), "subject": subject, "missing_count": target - len(vals)}],
            details={"observed_count": len(vals), "target_count": target},
        )
    return HandlerResult(details={"observed_count": len(vals), "target_count": target})


def handle_closure(rule, net, request):
    data = rule_dict(rule)
    scope = request.get("SCOPE")
    members = _closed_members(rule, scope)
    if request["OP"] == "CLOSURE":
        return HandlerResult(
            verdict=GO if members is not None else OPEN,
            details={"closed": members is not None, "members": sorted(members or ())},
        )
    rel = data["relation"]
    if members is None:
        return HandlerResult(verdict=OPEN, details={"closed": False})
    observed = {
        r.f("SUBJECT")
        for r in current_matches(net, predicate=rel["predicate"], object_=rel["target"])
    }
    return HandlerResult(
        verdict=GO if observed == members else BLOCK,
        conflicts=[] if observed == members else [{
            "rule": rule_addr(rule),
            "expected_members": sorted(members),
            "observed_members": sorted(observed),
        }],
        details={"closed": True},
    )


def handle_at_most_one(rule, net, request):
    data = rule_dict(rule)
    predicates = set(data["predicates"])
    if request["OP"] == "VALIDATE_INCOMING":
        incoming = request["INCOMING"]
        pred = incoming.f("PREDICATE")
        if pred not in predicates:
            return HandlerResult(details={"applicable": False})
        vals = current_values(net, incoming.f("SUBJECT"), pred)
        distinct = set(vals + [incoming.f("OBJECT")])
        if len(distinct) > data["value_cardinality"]["maximum"]:
            return HandlerResult(
                verdict=BLOCK,
                conflicts=[{
                    "rule": rule_addr(rule),
                    "subject": incoming.f("SUBJECT"),
                    "predicate": pred,
                    "values": sorted(distinct, key=repr),
                }],
                details={"applicable": True},
            )
        return HandlerResult(details={"applicable": True})

    subject = request.get("SUBJECT")
    pred = request.get("PREDICATE")
    if pred not in predicates:
        return HandlerResult(details={"applicable": False})
    vals = set(current_values(net, subject, pred))
    if len(vals) > data["value_cardinality"]["maximum"]:
        return HandlerResult(
            verdict=BLOCK,
            conflicts=[{"rule": rule_addr(rule), "subject": subject, "predicate": pred, "values": sorted(vals, key=repr)}],
        )
    return HandlerResult(details={"applicable": True, "values": sorted(vals, key=repr)})


def _pattern_match(net, pattern, bound_subject=None, force_binding=False):
    subject = bound_subject if force_binding else pattern.get("subject")
    return current_matches(net, subject, pattern["predicate"], pattern["object"])


def handle_implication(rule, net, request):
    data = rule_dict(rule)
    op = request["OP"]
    incoming = request.get("INCOMING")
    if op == "VALIDATE_INCOMING" and incoming is not None:
        ant = data["antecedent"]
        if incoming.f("PREDICATE") != ant["predicate"] or incoming.f("OBJECT") != ant["object"]:
            return HandlerResult(details={"applicable": False})
        subject = incoming.f("SUBJECT")
        antecedent_present = True
    else:
        subject = request.get("SUBJECT")
        antecedent_present = bool(_pattern_match(
            net,
            data["antecedent"],
            bound_subject=subject,
            force_binding=data.get("subject_binding") in ("same_link", "same_subject"),
        ))

    if not antecedent_present:
        return HandlerResult(details={"applicable": False})

    cons = data["consequent"]
    exact = current_matches(net, subject, cons["predicate"], cons["object"])
    if exact:
        return HandlerResult(details={"applicable": True, "consequent_holds": True})

    competitors = current_matches(net, subject, cons["predicate"])
    if competitors:
        return HandlerResult(
            verdict=BLOCK,
            conflicts=[{
                "rule": rule_addr(rule),
                "subject": subject,
                "required": (subject, cons["predicate"], cons["object"]),
                "current_objects": [r.f("OBJECT") for r in competitors],
            }],
            details={"applicable": True, "consequent_holds": False},
        )

    return HandlerResult(
        verdict=NEED,
        stops=[{
            "rule": rule_addr(rule),
            "missing": (subject, cons["predicate"], cons["object"]),
            "reason": "required consequent is not current",
        }],
        details={"applicable": True, "consequent_holds": False},
    )


def handle_balance(rule, net, request):
    data = rule_dict(rule)
    scope = request.get("SCOPE")
    if scope in set(data["balance"].get("excluded_nodes", [])):
        return HandlerResult(details={"applicable": False, "excluded": True})

    left, right = _equality_sides(net, rule, scope)
    if request["OP"] == "CHECK":
        if left["complete"] and right["complete"]:
            if left["value"] == right["value"]:
                return HandlerResult(details={"left": left["value"], "right": right["value"], "equal": True})
            closure = _closure_rule_for(rule, net)
            closed = _closed_members(closure, scope) is not None
            if not closed:
                return HandlerResult(
                    verdict=OPEN,
                    opens=[{"rule": rule_addr(rule), "scope": scope, "reason": "mismatch under open membership"}],
                    details={"left": left["value"], "right": right["value"], "equal": False, "closed": False},
                )
            return HandlerResult(
                verdict=BLOCK,
                conflicts=[{"rule": rule_addr(rule), "scope": scope, "left": left["value"], "right": right["value"]}],
                details={"equal": False, "closed": True},
            )
        return HandlerResult(
            verdict=OPEN,
            opens=[{"rule": rule_addr(rule), "scope": scope, "reason": "incomplete numeric expression"}],
            details={"left_complete": left["complete"], "right_complete": right["complete"]},
        )

    if request["OP"] != "DERIVE":
        raise SchemaError("balance handler supports CHECK or DERIVE")

    closure = _closure_rule_for(rule, net)
    closed_members = _closed_members(closure, scope)
    if closed_members is None:
        return HandlerResult(
            verdict=NEED,
            stops=[{"rule": rule_addr(rule), "missing": "declared closed membership"}],
        )

    candidates = []
    for side_name, side, other in (("left", left, right), ("right", right, left)):
        missing = set(side["missing_subjects"])
        if len(missing) != 1:
            continue
        if not other["complete"]:
            continue
        target_subject = next(iter(missing))
        derived_value = other["value"] - side.get("known_sum", 0)
        candidates.append((side_name, target_subject, side["value_predicate"], derived_value, side, other))

    if len(candidates) != 1:
        return HandlerResult(
            verdict=NEED,
            stops=[{"rule": rule_addr(rule), "missing": "exactly one derivable numeric value"}],
            details={"candidate_count": len(candidates)},
        )

    _, subject, predicate, value, side, other = candidates[0]
    requested_pred = request.get("PREDICATE")
    requested_subject = request.get("SUBJECT")
    if requested_pred is not None and requested_pred != predicate:
        return HandlerResult(
            verdict=NEED,
            stops=[{"rule": rule_addr(rule), "missing": "requested field is not the derivable numeric field"}],
            details={"derivable_predicate": predicate},
        )
    if requested_subject is not None and requested_subject != subject:
        return HandlerResult(
            verdict=NEED,
            stops=[{"rule": rule_addr(rule), "missing": "requested subject is not the unique missing subject"}],
            details={"derivable_subject": subject},
        )

    derived_addr = request.get("DERIVED_ADDR")
    if not derived_addr:
        return HandlerResult(verdict=NEED, stops=[{"rule": rule_addr(rule), "missing": "derived record address"}])

    rec = Record(derived_addr, {"SUBJECT": subject, "PREDICATE": predicate, "OBJECT": value})
    premises = sorted({r.addr for r in side["records"] + other["records"]})
    if closure is not None:
        premises.append(rule_addr(closure))
    provenance = premises + [rule_addr(rule)]
    return HandlerResult(
        verdict=GO,
        proposed_delta=[rec],
        derived_records=[rec],
        provenance_requirements=provenance,
        details={"derived": (subject, predicate, value), "premises": premises},
    )


HANDLERS = {
    "EXACT_DISTINCT_TARGET_CARDINALITY": handle_exact_cardinality,
    "CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION": handle_balance,
    "EXPLICIT_CLOSED_RELATION_SET": handle_closure,
    "CURRENT_VALUE_AT_MOST_ONE": handle_at_most_one,
    "CURRENT_STATUS_IMPLIES_MAGNITUDE": handle_implication,
}


class FamilyExecutor:
    def __init__(self, family_dictionary):
        self.dictionary = family_dictionary

    def supports(self, rule):
        return rule_type(rule) in HANDLERS

    def execute(self, rule, net, operation_request):
        rtype = rule_type(rule)
        spec = self.dictionary["families"].get(rtype)
        if spec is None or rtype not in HANDLERS:
            return HandlerResult(
                verdict=NEED,
                classification="EXECUTOR_HOLE",
                unchecked_dependencies=[{
                    "dependency": rule_addr(rule),
                    "reason": "EXECUTOR_HOLE",
                }],
            )

        errors = schema_contract_errors(rule, spec)
        if errors:
            return HandlerResult(
                verdict=NEED,
                classification="SCHEMA_DRIFT",
                unchecked_dependencies=[{
                    "dependency": rule_addr(rule),
                    "reason": "SCHEMA_DRIFT",
                }],
                details={"schema_errors": errors},
            )

        if operation_request["OP"] not in spec["operations"]:
            return HandlerResult(
                verdict=NEED,
                stops=[{"rule": rule_addr(rule), "missing": f"operation {operation_request['OP']}"}],
            )

        try:
            return HANDLERS[rtype](rule, net, operation_request)
        except (SchemaError, KeyError, TypeError, ValueError) as exc:
            return HandlerResult(
                verdict=NEED,
                classification="SCHEMA_DRIFT",
                unchecked_dependencies=[{
                    "dependency": rule_addr(rule),
                    "reason": "SCHEMA_DRIFT",
                }],
                details={"schema_exception": type(exc).__name__, "schema_message": str(exc)},
            )

    def validation_dependencies(self, net, incoming):
        deps = []
        for rule in network_rules(net):
            rtype = rule_type(rule)
            spec = self.dictionary["families"].get(rtype)
            if spec is not None and dependency_match(rule, spec, incoming):
                deps.append(rule)
        return deps

    def validate_incoming(self, net, incoming, marker_prefix="UNCHECKED"):
        """Validate an incoming record and make unexecutable checks visible."""
        results = []
        markers = []
        unchecked = []
        marker_n = 0

        for rule in network_rules(net):
            rtype = rule_type(rule)
            spec = self.dictionary["families"].get(rtype)

            if spec is None or rtype not in HANDLERS:
                reason = "EXECUTOR_HOLE"
                applicable = True  # dependency relevance cannot be ruled out
            else:
                preds = dependency_predicates(rule, spec)
                if not preds:
                    reason = "SCHEMA_DRIFT"
                    applicable = True  # malformed signature cannot rule dependency out
                else:
                    reason = None
                    applicable = incoming.f("PREDICATE") in preds

            if not applicable:
                continue

            if reason is not None:
                marker_n += 1
                marker = unchecked_marker(
                    f"{marker_prefix}_{marker_n}",
                    rule_addr(rule),
                    reason,
                )
                markers.append(marker)
                unchecked.append({"dependency": rule_addr(rule), "reason": reason})
                continue

            result = self.execute(rule, net, {"OP": "VALIDATE_INCOMING", "INCOMING": incoming})
            results.append({"rule": rule_addr(rule), "result": result})
            if result.classification in ("EXECUTOR_HOLE", "SCHEMA_DRIFT"):
                marker_n += 1
                marker = unchecked_marker(
                    f"{marker_prefix}_{marker_n}",
                    rule_addr(rule),
                    result.classification,
                )
                markers.append(marker)
                unchecked.append({
                    "dependency": rule_addr(rule),
                    "reason": result.classification,
                })

        return HandlerResult(
            verdict=NEED if unchecked else GO,
            proposed_delta=markers,
            unchecked_dependencies=unchecked,
            details={"rule_results": results},
        )
