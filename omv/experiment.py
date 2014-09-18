from analyzers import OMVAnalyzers


class OMVExperiment(object):
    def __init__(self, name, experiment, observables, backend, omt_root):
        self.name = name
        self.checks = {}
        self.results = None

        for obsname, observable in observables.iteritems():
            # an experiment can have multiple observables
            expected = experiment['expected'].get(obsname)
            self.checks[obsname] = OMVAnalyzers[obsname](observable, expected,
                                                         backend, omt_root)
            
    def check_all(self):
        return {n: c() for n, c in self.checks.iteritems()}
    
        
