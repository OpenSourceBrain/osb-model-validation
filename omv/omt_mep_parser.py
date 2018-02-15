from omv.experiment import OMVExperiment
from os.path import join, dirname
from omv.common.inout import load_yaml


class OMVParseError(BaseException):
    pass


class OMVTestParser(object):
    def __init__(self, omt_path):
        self.omt_path = omt_path
        self.omt_root = dirname(omt_path)
        self.omt = load_yaml(omt_path)
        if 'mep' in self.omt:
            self.mep_path = join(self.omt_root, self.omt['mep'])
            self.mep_root = dirname(self.mep_path)
            self.mep = load_yaml(self.mep_path)
        else:
            self.mep_root = None 
            self.mep_path = None
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

    def generate_exps(self, engine):
        if self.mep:
            for expname, exp in self.omt_experiments.items():
                expmep = self.mep_experiments[expname]
                obs = exp['observables']
                yield OMVExperiment(expname, expmep, obs,
                                    engine, self.omt_root, self.mep_root)
        else:
            exp = {'expected': {'dry': None}}
            obs = {'dry': None}
            yield OMVExperiment('Dry run', exp, obs,
                                engine, self.omt_root, self.mep_root)
