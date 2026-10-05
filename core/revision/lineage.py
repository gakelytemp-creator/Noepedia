# Policy lineage helpers.

def build_lineage(objects, relations):
    policies={o['id']:dict(o) for o in objects if o.get('type')=='META_POLICY'}
    parents={}
    children={}
    restores={}
    for r in relations:
        s=r.get('subject'); p=r.get('predicate'); o=r.get('object')
        if p=='DERIVED_FROM_META_POLICY':
            parents[s]=o
            children.setdefault(o,[]).append(s)
        elif p=='RESTORES_DEFINITION_FROM':
            restores[s]=o
    return {'policies':policies,'parents':parents,'children':children,'restore_sources':restores}

def ancestors(lineage, policy_id):
    out=[]
    seen=set()
    cur=policy_id
    while cur in lineage['parents']:
        cur=lineage['parents'][cur]
        if cur in seen:
            raise ValueError('cycle detected')
        seen.add(cur)
        out.append(cur)
    return out

def descendants(lineage, policy_id):
    out=[]
    queue=list(lineage['children'].get(policy_id,[]))
    seen=set()
    while queue:
        cur=queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        out.append(cur)
        queue.extend(lineage['children'].get(cur,[]))
    return out

def checkout_policy(lineage, policy_id):
    if policy_id not in lineage['policies']:
        raise KeyError(policy_id)
    return {
        'record_type':'META_POLICY_HISTORICAL_CHECKOUT',
        'policy_id':policy_id,
        'policy':dict(lineage['policies'][policy_id]),
        'ancestors':ancestors(lineage,policy_id),
        'descendants':descendants(lineage,policy_id),
        'restore_source':lineage['restore_sources'].get(policy_id),
        'read_only':True,
        'live_policy_mutated':False
    }

def compare_policy_definitions(lineage, left_id, right_id):
    left=lineage['policies'][left_id].get('definition',{})
    right=lineage['policies'][right_id].get('definition',{})
    keys=sorted(set(left)|set(right))
    changes=[]
    for k in keys:
        lv=left.get(k); rv=right.get(k)
        if lv!=rv:
            changes.append({'field':k,'left':lv,'right':rv})
    return {'record_type':'META_POLICY_DIFF','left_id':left_id,'right_id':right_id,'changes':changes,'change_count':len(changes)}

def trace_lineage(lineage, start_id, end_id):
    path=[end_id]
    cur=end_id
    seen=set()
    while cur!=start_id:
        if cur in seen or cur not in lineage['parents']:
            return None
        seen.add(cur)
        cur=lineage['parents'][cur]
        path.append(cur)
    path.reverse()
    return path
