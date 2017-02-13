from omv.analyzers.analyzer import OMVAnalyzer
from omv.analyzers.utils import timeseries as ts
from omv.analyzers.utils import filenode as fn
from omv.common.inout import inform


class InputResAnalyzer(OMVAnalyzer):
    """
    Input resistance
    """

    
    def parseOMT(self, to_parse):
        f = fn.FileNodeHelper(to_parse['file_Vm'], self.omt_root)
        f_i = fn.FileNodeHelper(to_parse['file_VC_i'], self.omt_root)
        inform('Calculating input resistance from files:',
               (f.filename,f_i.filename), indent=1, verbosity=1)
        h_voltage = to_parse.get('holding voltage', -70.)
        cmd_voltage = to_parse.get('command voltage', -80.)
        h_window = to_parse.get('holding window', [0., 0.])
        cmd_window = to_parse.get('command window', [0., 0.])

        # h_window = [float(t) for t in to_parse.get('holding window', [0., 0.])[0].split()]
        # cmd_window = [float(t) for t in to_parse.get('command window', [0., 0.])[0].split()]
        inform('Time wondow used for detection of current injections:',
               (h_window,cmd_window), indent=2, verbosity=1)
        input_resistance = ts.input_resistance(f.get_timeseries(), f_i.get_timeseries(), h_window, cmd_window, (h_voltage,cmd_voltage))
        return input_resistance
    
    def parse_expected(self):
        return self.expected

    def parse_observable(self):
        return self.parseOMT(self.observable)




















