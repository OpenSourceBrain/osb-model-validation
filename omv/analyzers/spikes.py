from omv.analyzers.analyzer import OMVAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.analyzers.utils import filenode as fn
from omv.common.inout import inform
from os import getcwd


class SpikeAnalyzer(OMVAnalyzer):

    def before_running(self):
        if 'file' in self.observable:
            self.f = fn.FileNodeHelper(self.observable['file'], self.omt_root)
            if self.f.tstamp:
                inform('Attention! Preexistent datafile: ', self.f.filename,
                       indent=2, verbosity=1)
        if 'spiketimes file' in self.observable:
            self.f = fn.SpikeFileNodeHelper(self.observable['spiketimes file'], self.omt_root)
            if self.f.tstamp:
                inform('Attention! Preexistent datafile: ', self.f.filename,
                       indent=2, verbosity=1)

    def parse_spikes(self, to_parse):
        spikes = []
        if isinstance(to_parse, list):
            spikes = to_parse
        elif 'file' in to_parse or 'spiketimes file' in to_parse:
            if not self.f.exists():
                inform('ERROR! Datafile %s does not exist (relative to %s)!'%
                        (self.f.filename, getcwd()), indent=2, verbosity=0, underline='-')
                spikes = None
            elif not self.f.has_changed():
                inform('ERROR! Datafile %s has not changed!'
                       % self.f.filename, indent=2, verbosity=0, underline='-')
                spikes = None
            elif self.f.has_changed():
                if 'file' in to_parse:
                    try:
                        tv = self.f.get_timeseries()
                    except Exception as e:
                        inform('ERROR! Could not read spikes from datafile %s (%s)!'
                           % (self.f.filename,e), indent=2, verbosity=0, underline='-')
                        spikes = []
                        return spikes
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
                    else:  # file contains spike times
                        spikes = tv
                        
                elif 'spiketimes file' in to_parse:
                    inform('Reading spiketimes from: ', self.f,
                           indent=1, verbosity=1)
                    all_spikes = self.f.get_spike_times()
                    if len(all_spikes)!=1:
                        inform('ERROR! Spike times file %s should contain only spikes for one cell!'
                           % (self.f.filename), indent=2, verbosity=0, underline='-')
                        return None
                    
                    spikes = list(all_spikes.values())[0]
            else:
                inform('ERROR! Preexistent datafile %s has not been updated!'
                       % self.f.filename, indent=2, verbosity=0, underline='-')
                spikes = []
        return spikes

    def parse_expected(self):
        return self.parse_spikes(self.expected)

    def parse_observable(self):
        return self.parse_spikes(self.observable)










