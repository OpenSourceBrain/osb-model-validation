import yaml
from backends import OMVBackends
from analyzers import OMVAnalyzers
from common.output import inform
from os.path import join, dirname

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
    omt_root = dirname(omt_path)
    if impl:
        mepfile = join(omt_root, impl['mep'])
        observables = impl['observables']
        mep = load_yaml(mepfile) 
        experiment = mep['experiments'][impl['experiment']]
    else:
        observables = {'dry':None} 
        experiment = {'expected':{'dry':None}}

    backend = OMVBackends[engine](join(omt_root, target))
    for obsname, observable in observables.iteritems():
        expected = experiment['expected'].get(obsname, None)
        tests.append(OMVAnalyzers[obsname](observable, expected, backend, omt_root))

    backend.run()
    return [t() for t in tests]
    


if __name__ == '__main__':
    import sys
    t = parse_omt(sys.argv[1])
    print 'Test results:', t
    exit(not all(t))
    
    












