from omv.analyzers.analyzer import OMVAnalyzer
from omv.common.inout import inform


class DryRunAnalyzer(OMVAnalyzer):
    
    def __init__(self, ost, expected, engine, omt_root, mep_root):
        inform('No mep file specified. Will only run simulation using: ',
               engine, indent=1)
        self.engine = engine

    def __call__(self):
        return not self.engine.returncode













