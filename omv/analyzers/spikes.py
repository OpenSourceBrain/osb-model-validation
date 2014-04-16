from analyzer import OMVAnalyzer
from utils import timeseries as ts
from ..common.output import inform

class SpikeAnalyzer(OMVAnalyzer):
    
    def parse_spikes(self, to_parse):
        if isinstance(to_parse, list):
            spikes = to_parse
        elif 'file' in to_parse:
            tv = ts.timeseries_from_file_node(to_parse['file'])
            if 'spike detection' in to_parse:
                sd = to_parse['spike detection']
                method = sd.get('method', 'threshold')
                threshold = float(sd.get('threshold', 0))
                inform('Detecting spikes from file', to_parse['file'], indent=1)
                spikes = ts.spikes_from_timeseries(tv, method=method, threshold=threshold)
        return spikes

    def parse_expected(self):
        return self.parse_spikes(self.expected)

    def parse_observable(self):
        return self.parse_spikes(self.observable)
















