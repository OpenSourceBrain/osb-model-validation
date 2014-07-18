from analyzer import OMVAnalyzer
from utils import timeseries as ts
from ..common.output import inform

class DryRunAnalyzer(OMVAnalyzer):
    
    def __init__(self, ost, expected, backend, omt_root):
        inform('No mep file specified. Will only run simulation using: %s.'%backend, indent=1)
        self.backend = backend

    def __call__(self):
        return not self.backend.returncode













