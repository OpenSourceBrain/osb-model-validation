from analyzer import OMVAnalyzer
from utils import timeseries as ts
from utils import filenode as fn
from ..common.inout import inform


class SpikeAnalyzer(OMVAnalyzer):

    def before_running(self):
        if 'file' in self.observable:
            self.f = fn.FileNodeHelper(self.observable['file'], self.omt_root)
            if self.f.tstamp:
                inform('Attention! Preexistent datafile: ', self.f.filename,
                       indent=2, verbosity=1)

    def parse_spikes(self, to_parse):
        if isinstance(to_parse, list):
            spikes = to_parse
        elif 'file' in to_parse:
            if self.f.has_changed():
                tv = self.f.get_timeseries()
                inform('Reading timeseries from: ', self.f,
                       indent=1, verbosity=1)
                if 'spike detection' in to_parse:
                    sd = to_parse['spike detection']
                    method = sd.get('method', 'threshold')
                    threshold = float(sd.get('threshold', 0))
                    inform('Detecting spikes with method: ',
                           method, indent=2, verbosity=1)
                    spikes = ts.spikes_from_timeseries(tv, method=method,
                                                       threshold=threshold)
            else:
                inform('ERROR! Preexistent datafile %s has not been updated!'
                       % self.f.filename, indent=2, verbosity=0, underline='-')
                spikes = []
        return spikes

    def parse_expected(self):
        return self.parse_spikes(self.expected)

    def parse_observable(self):
        return self.parse_spikes(self.observable)










