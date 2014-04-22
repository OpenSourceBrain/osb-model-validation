import utils.timeseries as ts
from ..common.output import inform

class OMVAnalyzer(object):
    def __init__(self, observable, expected, backend):
        self.backend = backend
        self.observable = observable
        self.expected = expected
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
        except (TypeError, KeyError) as e: #observable can be None 
            tolerance =  1e-1

        are_close = ts.compare_arrays((obs, exp), tolerance)
        if not are_close:
            inform('Comparison of \n %s \n and \n %s \n failed against tolerance %g'%(obs,exp, tolerance))
        
        return are_close
