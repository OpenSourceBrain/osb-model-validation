import yaml
from backends import OMVBackends
from experiment import OMVExperiment
from os.path import join, dirname
from common.output import inform


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
    

class OMVTestParser(object):
    def __init__(self, omt_path):
        self.omt_root = dirname(omt_path)
        self.omt = load_yaml(omt_path)
        if 'mep' in self.omt:
            mep_path = join(self.omt_root, self.omt['mep'])
            self.mep = load_yaml(mep_path)
        else:
            self.mep = None
            
    @property
    def modelpath(self):
        return join(self.omt_root, self.omt['target'])

    @property
    def engine(self):
        return self.omt['engine']
    
    @property
    def mep_experiments(self):
        return self.mep['experiments']

    @property
    def omt_experiments(self):
        return self.omt['experiments']

    def generate_exps(self, backend):
        if self.mep:
            for expname, exp in self.omt_experiments.iteritems():
                expmep = self.mep_experiments[expname]
                obs = exp['observables']
                yield OMVExperiment(expname, expmep, obs,
                                    backend, self.omt_root)
        else:
            exp = {'expected': {'dry': None}}
            obs = {'dry': None}
            yield OMVExperiment('Dry run', exp, obs,
                                backend, self.omt_root)


class OMVTestSuite(object):
    def __init__(self, omt_path):
        mepomt = OMVTestParser(omt_path)
        self.backend = OMVBackends[mepomt.engine](mepomt.modelpath)
        self.experiments = [exp for exp in mepomt.generate_exps(self.backend)]

    def run(self):
        self.backend.run()

        inform('running checks for experiments ',
               [exp.name for exp in self.experiments], indent=2)
        results = []
        for exp in self.experiments:
            results.append([check() for check in exp.checks])
        return results


def parse_omt(omt_path):
    return OMVTestSuite(omt_path).run()
    

    
    


