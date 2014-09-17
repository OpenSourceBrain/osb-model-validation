from analyzer import OMVAnalyzer
from ..common.io import inform


class DryRunAnalyzer(OMVAnalyzer):
    
    def __init__(self, ost, expected, backend, omt_root):
        inform('No mep file specified. Will only run simulation using:',
               backend, indent=1)
        self.backend = backend

    def __call__(self):
        return not self.backend.returncode













