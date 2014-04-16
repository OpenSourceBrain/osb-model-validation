from analyzer import OMVAnalyzer
from utils import timeseries as ts
from ..common.output import inform

class RestingAnalyzer(OMVAnalyzer):

    def parse_resting(self, to_parse):
        if isinstance(to_parse, (int, float)):
            inform('Explicit resting potential specified' , indent=1)
            resting = to_parse
        elif 'file' in to_parse:
            inform('Calculating resting potential from file', to_parse['file'], indent=1)
            resting = ts.resting_from_file_node(to_parse['file'])
        return resting
    
    def parse_expected(self):
        return self.parse_resting(self.expected)

    def parse_observable(self):
        return self.parse_resting(self.observable)




















