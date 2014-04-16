import utils.timeseries as ts

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

        return ts.compare_arrays((obs, exp), tolerance)
