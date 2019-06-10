from omv.analyzers.utils.timeseries import *
from omv.common.inout import inform


class OMVAnalyzer(object):
    def __init__(self, observable, expected, engine, omt_root, mep_root):
        self.engine = engine
        self.observable = observable
        self.expected = expected
        self.omt_root = omt_root
        self.mep_root = mep_root
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
            if obs is None:
                    inform("Could not determine observed values")
                    return False
            if isinstance(obs, list):
                for o in obs:
                    if not o:
                        inform("Could not determine observed values")
                        return False
                    
            exp = self.parse_expected()
            
            if exp is None:
                    inform("Could not determine expected values, value None")
                    return False
            if isinstance(exp, list):
                for e in exp:
                    if not e:
                        inform("Could not determine expected values")
                        return False
        except IOError as e:
            inform("Input/output error when\
                   checking for observable data: %s" % e)
            return False
        
        try:
            tolerance = float(self.observable['tolerance'])
        except (TypeError, KeyError):  # observable can be None
            tolerance = 1e-1

        are_close, best_tol = compare_arrays((obs, exp), tolerance)

        if not are_close:
            pretty_obs, pretty_exp = pretty_print_copypaste(obs,exp)
            inform("Comparison of \n\
                    (observed data): %s\n\
                    and\n\
                    (expected data): %s\n\
                    failed against tolerance %g" %
                   (pretty_obs, pretty_exp, tolerance))
            if best_tol:
                inform("A better tolerance to try is: ", best_tol, indent=1)
        else:
            if best_tol and best_tol < tolerance:
                inform("Passed, but an even better tolerance might be: %s, as opposed to: %s (diff: %s)" % (best_tol, tolerance,(tolerance-best_tol)), indent=3, verbosity=1)
        return are_close
