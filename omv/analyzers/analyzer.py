import utils.timeseries as ts
from ..common.inout import inform


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
        
        try:
            obs = self.parse_observable()
            exp = self.parse_expected()
        except IOError as e:
            inform("Input/output error when\
                   checking for observable data: %s" % e)
            return False
        
        try:
            tolerance = float(self.observable['tolerance'])
        except (TypeError, KeyError):  # observable can be None
            tolerance = 1e-1

        are_close, best_tol = ts.compare_arrays((obs, exp), tolerance)
        if not are_close:
            try:  # making it easier to copy/paste lists
                pretty_obs = [float(el) for el in obs]
                pretty_exp = [float(el) for el in exp]
            except TypeError:  # obs,exp can be singletons
                pretty_obs, pretty_exp = map(float, (obs, exp))
            inform("Comparison of \n\
                    (observed data): %s\n\
                    and\n\
                    (expected data): %s\n\
                    failed against tolerance %g" %
                   (pretty_obs, pretty_exp, tolerance))
            if len(obs) == len(exp):
                inform("A better tolerance to try is: ", best_tol, indent=1)
        else:
            if best_tol < tolerance:
                inform("Passed, but an even better tolerance might be: %f, as opposed to: %f" % (best_tol, tolerance), indent=3, verbosity=1)
        return are_close
