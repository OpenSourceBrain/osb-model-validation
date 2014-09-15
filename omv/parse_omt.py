import yaml
from backends import OMVBackends
from experiment import OMVExperiment
from os.path import join, dirname


class OMVTestSuite(object):
    def __init__(self, omt_path):
        omt = load_yaml(omt_path)

        omt_root = dirname(omt_path)
        modelpath = join(omt_root, omt['target'])
        self.backend = OMVBackends[omt['engine']](modelpath)

        impl = omt.get('implements')
        if impl:
            mepfile = join(omt_root, impl['mep'])
            observables = impl['observables']
            mep = load_yaml(mepfile)
            experiment = mep['experiments'][impl['experiment']]
        else:
            # dry runs don't implement mep files
            observables = {'dry': None}
            experiment = {'expected': {'dry': None}}
        self.experiments = OMVExperiment(experiment,
                                         observables, self.backend, omt_root)

    def run(self):
        self.backend.run()
        return [check() for check in self.experiments.checks]


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y


def parse_omt(omt_path):
    return OMVTestSuite(omt_path).run()
    

    
    


