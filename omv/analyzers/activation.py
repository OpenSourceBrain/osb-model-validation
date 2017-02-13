from omv.analyzers.analyzer import OMVAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.analyzers.utils import filenode as fn
from omv.common.inout import inform


class ActivationVariableAnalyzer(OMVAnalyzer):

    def parse_observable(self):
        if 'file' in self.observable:
            f = fn.FileNodeHelper(self.observable['file'], self.omt_root)
            inform('Activation variable from file',
                   self.observable['file'], indent=1, verbosity=1)
            return f.get_timeseries()
    
    def __call__(self):
        obs = self.parse_observable()
        allin = ts.all_within_bounds(obs, (0, 1))
        if not allin:
            inform('Activation variable outside of (0,1) interval: ',
                   obs, indent=1)
        return allin




















