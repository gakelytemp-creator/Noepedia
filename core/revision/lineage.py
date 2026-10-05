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
