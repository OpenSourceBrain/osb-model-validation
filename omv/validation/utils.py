def topological_sort(source):
    """perform topo sort on elements.

    :arg source: list of ``(name, [list of dependancies])`` pairs
    :returns: list of names, with dependancies listed first
    """
    pending = [(name, set(deps)) for name, deps in source] # copy deps so we can modify set in-place       
    emitted = []        
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            name, deps = entry
            deps.difference_update(emitted) # remove deps we emitted last pass
            if deps: # still has deps? recheck during next pass
                next_pending.append(entry) 
            else: # no more deps? time to emit
                yield name 
                emitted.append(name) # <-- not required, but helps preserve original ordering
                next_emitted.append(name) # remember what we emitted for difference_update() in next pass
        if not next_emitted: # all entries have unmet deps, one of two things is wrong...
            raise ValueError("cyclic or missing dependancy detected: %r" % (next_pending,))
        pending = next_pending
        emitted = next_emitted
        

def all_types_in_schema(d):
    for k,v in d.items():
        if isinstance(v, dict):
            for x in all_types_in_schema(v):
                yield x
        elif isinstance(v, list):
            for el in v:
                for x in all_types_in_schema(el):
                    yield x
        else:
            try: 
                if v.startswith('/omv'):
                    yield v
            except AttributeError:
                pass













