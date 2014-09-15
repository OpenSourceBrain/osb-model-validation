import yaml
from backends import OMVBackends
from analyzers import OMVAnalyzers
from os.path import join, dirname


class OMVTestSuite(object):
    def __init__(self, omt_path):
        omt = load_yaml(omt_path)
        omt_root = dirname(omt_path)
        engine = omt['engine']
        target = omt['target']
        self.backend = OMVBackends[engine](join(omt_root, target))

        impl = omt.get('implements')
        if impl:
            mepfile = join(omt_root, impl['mep'])
            observables = impl['observables']
            mep = load_yaml(mepfile)
            experiment = mep['experiments'][impl['experiment']]
        else:
            observables = {'dry': None}
            experiment = {'expected': {'dry': None}}
        self.experiments = OMVExperiment(experiment,
                                         observables, self.backend, omt_root)

    def run(self):
        self.backend.run()
        return [check() for check in self.experiments.checks]


class OMVExperiment(object):
    def __init__(self, experiment, observables, backend, omt_root):
        self.observables = observables
        self.experiment = experiment
        self.checks = []
        for obsname, observable in observables.iteritems():
            # an experiment can have multiple observables,
            expected = experiment['expected'].get(obsname, None)
            self.checks.append(OMVAnalyzers[obsname]
                               (observable, expected, backend, omt_root))


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y

    
def parse_omt(omt_path):
    return OMVTestSuite(omt_path).run()
    

if __name__ == '__main__':
    import sys
    t = parse_omt(sys.argv[1])
    print 'Test results:', t
    exit(not all(t))
    
    


