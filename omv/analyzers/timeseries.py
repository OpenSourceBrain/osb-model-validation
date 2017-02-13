from omv.analyzers.analyzer import OMVAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.analyzers.utils import filenode as fn
from omv.common.inout import inform


class TimeSeriesAnalyzer(OMVAnalyzer):

    def before_running(self):
        if 'file' in self.observable:
            self.fo = fn.FileNodeHelper(self.observable['file'], self.omt_root)
            if self.fo.tstamp:
                inform('Attention! Preexistent datafile: ', self.fo.filename,
                       indent=2, verbosity=1)

    def parse_ts(self, to_parse):
        return ts

    def parse_expected(self):
        to_parse = self.expected
        if isinstance(to_parse, list):
            ts = to_parse
        elif 'file' in to_parse:
            f = fn.FileNodeHelper(to_parse['file'], self.mep_root)
            ts = f.get_timeseries()
            inform('Reading timeseries from: ', f, indent=1, verbosity=1)
        return ts

    def parse_observable(self):
        to_parse = self.observable
        if isinstance(to_parse, list):
            ts = to_parse
        elif 'file' in to_parse:
            if not self.fo.has_changed():
                inform('ERROR! Datafile %s does not exist!'
                       % self.fo.filename, indent=2, verbosity=0, underline='-')
                ts = []
            elif self.fo.has_changed():
                ts = self.fo.get_timeseries()
                inform('Reading timeseries from: ', self.fo,
                       indent=1, verbosity=1)
            else:
                inform('ERROR! Preexistent datafile %s has not been updated!'
                       % self.fo.filename, indent=2, verbosity=0, underline='-')
                ts = []
        return ts 










