from analyzer import OMVAnalyzer
from utils import timeseries as ts
from utils import filenode as fn
from ..common.output import inform

class SpikeAnalyzer(OMVAnalyzer):
    
    def parse_spikes(self, to_parse):
        if isinstance(to_parse, list):
            spikes = to_parse
        elif 'file' in to_parse:
            f = fn.FileNodeHelper(to_parse['file'])
            tv = f.get_timeseries()
            inform('Reading timeseries from:', f, indent=1)
            if 'spike detection' in to_parse:
                sd = to_parse['spike detection']
                method = sd.get('method', 'threshold')
                threshold = float(sd.get('threshold', 0))
                inform('Detecting spikes with method:', method, indent=2)
                spikes = ts.spikes_from_timeseries(tv, method=method, threshold=threshold)
        return spikes

    def parse_expected(self):
        return self.parse_spikes(self.expected)

    def parse_observable(self):
        return self.parse_spikes(self.observable)










