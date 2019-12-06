from omv.analyzers.spikes import SpikeAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.common.inout import inform
from os import getcwd


class RateAnalyzer(SpikeAnalyzer):

    def parse_spike_rates(self, to_parse):
        
        if isinstance(to_parse, float) or isinstance(to_parse, int):
            rate = to_parse
            
        elif 'file' in to_parse or 'spiketimes file' in to_parse:
            
            spikes = []
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
                           
                    spikes = self.f.get_spike_times()
                    
                if 'method' in to_parse:
                    method = to_parse['method']
                    if 'start_time' in to_parse:
                        start_time = to_parse['start_time']
                    else:
                        start_time=0
                    if 'end_time' in to_parse:
                        end_time = to_parse['end_time']
                    else:
                        end_time=float('inf')
                    rate = ts.get_spike_rate(spikes, method, start_time, end_time)
                    
                else:
                    rate = ts.get_spike_rate(spikes)
            else:
                inform('ERROR! Preexistent datafile %s has not been updated!'
                       % self.f.filename, indent=2, verbosity=0, underline='-')
                rate = -1
                
        return rate

    def parse_expected(self):
        return self.parse_spike_rates(self.expected)

    def parse_observable(self):
        return self.parse_spike_rates(self.observable)










