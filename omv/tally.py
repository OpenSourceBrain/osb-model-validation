from collections import OrderedDict
from yaml import dump


class Tallyman(object):
    def __init__(self, mepomt):
        self.omt = mepomt.omt_path
        self.mep = mepomt.mep_path
        self.backend = mepomt.engine
        self.modelpath = mepomt.modelpath
        self.experiments = {}

    def all_passed(self):
        alltrue = True if any(self.experiments) else False
        for res in self.experiments.values():
            alltrue = alltrue and all(res.values())
        return alltrue
        
    def add_experiment(self, exp, results):
        self.experiments[exp.name] = results

    def serialize(self):
        s = OrderedDict({'backend': self.backend})
        s['MEP file'] = self.mep
        s['OMT file'] = self.omt
        s['Model path'] = self.modelpath
        s['Experiments'] = self.experiments
        s['All Passed'] = self.all_passed()
        #return dump(s, default_flow_style=False)
        return s
