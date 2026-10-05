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
