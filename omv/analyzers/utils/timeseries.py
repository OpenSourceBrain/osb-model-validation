
from omv.common.inout import inform

def detect_spikes(v, method='threshold', threshold=0.):
    from numpy import flatnonzero, bitwise_and, roll, diff, array

    extrema = array([])
    if method == 'threshold':
        extrema = 1 + flatnonzero(bitwise_and((v[:-1] <= threshold),
                                          (roll(v, -1)[:-1] > threshold)))
    elif method == 'derivative':
        # This should only work for noiseless cases!
        dx = diff(v)
        extrema = 1 + flatnonzero(bitwise_and((dx[:-1] >= 0), (roll(dx, -1)[:-1] < 0)))
    else:
        print('still need to implement fancier spike detectors...')
        #see for example scipy.signal.find_peaks_cwt 
    return extrema


def load_data_file(fname, columns=(0, 1), header_lines=0, scaling=1):
    from numpy import loadtxt
    ts = loadtxt(fname, usecols=columns, skiprows=header_lines)
    return ts * scaling



def load_spike_file(fname, format='ID_TIME', ids=0, scaling=1.0):
    from numpy import loadtxt
    ts = loadtxt(fname)
    spike_map = {}
    for l in ts:
        if format=='ID_TIME':
            t = l[1]*scaling
            id = l[0]
        elif format=='TIME_ID':
            t = l[0]*scaling
            id = l[1]
        if ids==id or ids=='*':
            if not id in spike_map:
                spike_map[id] = []
            spike_map[id].append(t)
    return spike_map


def compare_arrays(arrays, tolerance):
    from numpy import allclose, array, max, abs, atleast_1d
    
    a1, a2 = array(arrays)
    
    if (hasattr(a1, '__len__') or hasattr(a2, '__len__')) and len(a1)!=len(a2):  # Different lengths!!
        return (False, 0)
    
    best_tol = None
    try:
        comp = allclose(a1, a2, tolerance)
        if len(atleast_1d(a1)) > 0:
            best_tol = max(abs((a1-a2)/a2))
    except ValueError:
        comp = False
    return (comp, best_tol)


def compare_dictionaries(d1, d2, tolerance=0.1):
    from numpy import allclose, array
    ks = d1.keys() if len(d1) < len(d2) else d2.keys()
    a1 = array([d1[k] for k in ks if k in d1])
    a2 = array([d2[k] for k in ks if k in d2])
    return allclose(a1, a2, tolerance)


def load_spike_times(spiketime):
    if isinstance(spiketime, list):
        return spiketime
    else:
        return load_data_file(spiketime, [0])


def spikes_from_timeseries(ts, **kwargs):
    method = kwargs.get('method', 'threshold')
    threshold = kwargs.get('threshold', 0)
    t, v = ts.T
    spk_idx = detect_spikes(v, method, threshold)
    return t[spk_idx]


def spikes_from_datafile(path, columns=(0, 1), header=0,
                         method='threshold', threshold=0):
    t, v = load_data_file(path, columns, header)
    spk_idx = detect_spikes(v, method, threshold)
    return t[spk_idx]


def average_resting(tv, window, col=1):
    from numpy import mean
    return mean(tv[-window:, col])


def input_resistance(tv, ti, h_window, cmd_window, voltages, col=1):
    from numpy import mean,where
    t = ti[:,0]
    #print(cmd_window
    t_holding = where((t >= h_window[0]) & (t <= h_window[1]))
    t_cmd = where((t >= cmd_window[0]) & (t <= cmd_window[1]))
    holding_i = mean(ti[t_holding, col])
    command_i = mean(ti[t_cmd, col])
    holding_v = mean(tv[t_holding, col])
    command_v = mean(tv[t_cmd, col])
    i_step = command_i - holding_i
    v_step = command_v - holding_v #voltages[0]-voltages[1]
    #print(v_step, i_step, holding_i, command_i
    input_resistance = v_step / i_step
    return input_resistance


def all_within_bounds(ts, bounds=(0, 1)):
    from numpy import all
    #print(type(bounds[0]),bounds[0],bounds[1], ts.size
    return all((ts[:, 1:] >= bounds[0]) & (ts[:, 1:] <= bounds[1]))


def all_nonzero(ts):
    from numpy import all
    return all(ts[:, 1:])


def pretty_print_copypaste(obs, exp):
    from numpy import atleast_1d
    ob = atleast_1d(obs) 
    ex = atleast_1d(exp) 
    suggest_tol = False
    try:  # making it easier to copy/paste lists
        pretty_obs = [float(el) for el in ob]
        pretty_exp = [float(el) for el in ex]
        suggest_tol = len(ob) == len(ex)
        
    except Exception as e: # obs, exp can be rank > 1. Not sure if we would ever c&p those
        pretty_obs, pretty_exp = (str(ob), str(ex))
        
    return pretty_obs, pretty_exp


def test_detect_spikes():
    from numpy import array, all, arange
    x = array([-1, 0, 1, 0] * 10)

    spk_idx = detect_spikes(x, method='derivative')
    assert all(spk_idx == arange(2, len(x), 4))

    spk_idx = detect_spikes(x, method='threshold', threshold=0.1)
    assert all(spk_idx == arange(2, len(x), 4))

    xx = -x # edge case: first point > threshold
    spk_idx = detect_spikes(xx, method='derivative')
    assert all(spk_idx == arange(4, len(xx), 4))

    spk_idx = detect_spikes(xx, method='threshold', threshold=0.1)
    assert all(spk_idx == arange(4, len(xx), 4))
    
    
def _get_single_spike_rate(spiketimes, method, start_time, end_time):
    
    
    if method==ISI_BASED_SPIKERATE_CALC:

        isis = []
        tot_isi = 0
        for si in range(len(spiketimes)-1):
            if spiketimes[si+1]>=start_time and spiketimes[si+1]<=end_time and \
               spiketimes[si]>=start_time and spiketimes[si]<=end_time:
                isi = spiketimes[si+1] - spiketimes[si]
                isis.append(isi)
                tot_isi+=isi 
        if len(isis)>0:
            rate = len(isis)/ float(tot_isi)
        else:
            rate=0
        inform('Spikes (%i): %s, qualifying ISIs: %s, rate: %s'%(len(spiketimes), spiketimes, isis, rate),verbosity=2, indent=2)
        
    elif method==DURATION_BASED_SPIKERATE_CALC:
        dur = float(end_time-start_time)
        spikes_in = 0
        for s in spiketimes:
            if s>=start_time and s<=end_time:
                spikes_in+=1
        rate = spikes_in/dur
        inform('Spikes %i of %i inside range %s->%s, so rate %s'%(spikes_in, len(spiketimes), start_time, end_time, rate),verbosity=2, indent=2)
        return rate
    
    else:
       raise Exception('Unknown method for calculating rates: %s'%method) 
        
    return rate
    
    
ISI_BASED_SPIKERATE_CALC = 'isi based'
DURATION_BASED_SPIKERATE_CALC = 'duration based'


def get_spike_rate(spikes, method=ISI_BASED_SPIKERATE_CALC, start_time=0, end_time=float('inf')):
    inform('Calculating average of %i spike rate(s) with method "%s" from %s->%s'%(len(spikes), method,start_time,end_time),verbosity=1, indent=2)
    
    if isinstance(spikes, list):
        return _get_single_spike_rate(spikes, method, start_time, end_time)
    
    if isinstance(spikes, dict):
        tot_rates = 0 
        all_rates = []
        if len(spikes)==0:
            avg_rate=0
        else:
            for s in spikes.values():
                r = _get_single_spike_rate(s, method, start_time, end_time)
                all_rates.append(r)
                tot_rates += r
            avg_rate = float(tot_rates)/len(spikes)
        inform('Calculated average of %i spike rate(s) with method "%s": %s %s'%(len(spikes), method, avg_rate, all_rates),verbosity=1, indent=2)
        return avg_rate


if __name__ == '__main__':
    
    from omv.common.inout import set_verbosity
    set_verbosity(2)
    
    tsNone = []
    tsA = [0.1]
    tsB = [0.1, 0.2]
    
    ts1 = [0.1,0.2,0.3,0.40]
    ts2 = [0.1,0.3,0.50]
    
    methods = [ISI_BASED_SPIKERATE_CALC, DURATION_BASED_SPIKERATE_CALC]
    
    for method in methods:

        opts = [tsNone, tsA, tsB, ts1, ts2, {'0':ts1}, {'0':ts1, '1':ts2}]
        for opt in opts:
            start_time = 0
            end_time = 0.25
            inform(' > Rate in %s->%s (%s) for %s: %s\n'%(start_time, end_time, method, opt,get_spike_rate(opt, method, start_time, end_time)), indent=2)


