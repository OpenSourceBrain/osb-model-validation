import yaml
from backends import OMVBackends
from analyzers import OMVAnalyzers
from common.output import inform

def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y

def parse_omt(omt_path):
    omt = load_yaml(omt_path)
    engine = omt['engine']
    target = omt['target']
    impl = omt.get('implements')

    inform('Running tests defined in:', omt_path)

    tests = []
    if impl:
        mepfile = impl['mep']
        observables = impl['observables']
        mep = load_yaml(mepfile) 
        experiment = mep['experiments'][impl['experiment']]
    else:
        observables = {'dry':None} 
        experiment = {'expected':{'dry':None}}

    backend = OMVBackends[engine](target)
    for obsname, observable in observables.iteritems():
        expected = experiment['expected'][obsname]
        tests.append(OMVAnalyzers[obsname](observable, expected, backend))

    backend.run()
    return [t() for t in tests]
    


if __name__ == '__main__':
    import sys
    t = parse_omt(sys.argv[1])
    print 'Test results:', t
    exit(not all(t))
    
    












