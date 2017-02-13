from omv.analyzers.analyzer import OMVAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.analyzers.utils import filenode as fn
from omv.common.inout import inform


class RestingAnalyzer(OMVAnalyzer):

    def parse_resting(self, to_parse):
        if isinstance(to_parse, (int, float)):
            resting = to_parse
            inform('Explicit resting potential specified:',
                   to_parse, indent=1, verbosity=1)
        elif 'file' in to_parse:
            f = fn.FileNodeHelper(to_parse['file'], self.omt_root)
            inform('Calculating resting potential from file:',
                   f.filename, indent=1, verbosity=1)
            window = to_parse.get('average last', 1)
            if window > 1:
                inform('Number of final points taken for averaging:',
                       window, indent=2, verbosity=1)
            resting = ts.average_resting(f.get_timeseries(), window)
        return resting
    
    def parse_expected(self):
        return self.parse_resting(self.expected)

    def parse_observable(self):
        return self.parse_resting(self.observable)




















