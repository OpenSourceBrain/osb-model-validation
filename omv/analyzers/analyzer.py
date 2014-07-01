import utils.timeseries as ts
from ..common.output import inform

class OMVAnalyzer(object):
    def __init__(self, observable, expected, backend, omt_root):
        self.backend = backend
        self.observable = observable
        self.expected = expected
        self.omt_root = omt_root
        self.before_running()

    def before_running(self):
        pass

    def parse_expected(self):
        pass

    def parse_observable(self):
        pass

    def __call__(self):
        obs = self.parse_observable()
        exp = self.parse_expected()
        try: 
            tolerance = float(self.observable['tolerance'])
        except (TypeError, KeyError): #observable can be None 
            tolerance =  1e-1

        are_close = ts.compare_arrays((obs, exp), tolerance)
        if not are_close:
            inform('Comparison of \n(observed data): %s\nand\n(expected data): %s\nfailed against tolerance %g'%([float(o) for o in obs],exp, tolerance))
        
        return are_close
