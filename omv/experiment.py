from analyzers import OMVAnalyzers


class OMVExperiment(object):
    def __init__(self, name, experiment, observables, backend, omt_root):
        self.name = name
        self.checks = []

        for obsname, observable in observables.iteritems():
            # an experiment can have multiple observables
            expected = experiment['expected'].get(obsname)
            self.checks.append(OMVAnalyzers[obsname]
                               (observable, expected, backend, omt_root))
            
    def check_all(self):
        self.results = [c() for c in self.checks]
