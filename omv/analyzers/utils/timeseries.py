def detect_spikes(v, method='threshold', threshold=0.):
    from numpy import flatnonzero, bitwise_and, roll, diff, array

    extrema = array([])

    if method == 'threshold':
        extrema = flatnonzero(bitwise_and((v[:-1] <= threshold),
                                          (roll(v, -1)[:-1] > threshold)))
    elif method == 'derivative':
        # This should only work for noiseless cases!
	dx = diff(v)
        extrema = 1 + flatnonzero(bitwise_and((dx[:-1] >= 0), (roll(dx, -1)[:-1] < 0)))
    else:
        print 'still need to implement fancier spike detectors...'
        #see for example scipy.signal.find_peaks_cwt 
    return extrema


def load_data_file(fname, columns=(0, 1), header_lines=0, scaling=1):
    from numpy import loadtxt
    ts = loadtxt(fname, usecols=columns, skiprows=header_lines)
    return ts * scaling


def compare_arrays(arrays, tolerance):
    from numpy import allclose, array, max, abs

    a1, a2 = array(arrays)
    best_tol = None
    try:
        comp = allclose(a1, a2, tolerance)
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
    #print cmd_window
    t_holding = where((t >= h_window[0]) & (t <= h_window[1]))
    t_cmd = where((t >= cmd_window[0]) & (t <= cmd_window[1]))
    holding_i = mean(ti[t_holding, col])
    command_i = mean(ti[t_cmd, col])
    holding_v = mean(tv[t_holding, col])
    command_v = mean(tv[t_cmd, col])
    i_step = command_i - holding_i
    v_step = command_v - holding_v #voltages[0]-voltages[1]
    #print v_step, i_step, holding_i, command_i
    input_resistance = v_step / i_step
    return input_resistance
    

def all_within_bounds(ts, bounds=(0, 1)):
    from numpy import all
    #print type(bounds[0]),bounds[0],bounds[1], ts.size
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
    except TypeError: # obs, exp can be rank > 1. Not sure if we would ever c&p those
	pretty_obs, pretty_exp = (str(ob), str(ex))
    return pretty_obs, pretty_exp, suggest_tol


def test_detect_spikes():
    from numpy import array, all, arange
    x = array([-1, 0, 1, 0] * 10)

    spk_idx = detect_spikes(x, method='derivative')
    assert all(spk_idx == arange(2, len(x), 4))

    spk_idx = detect_spikes(x, method='threshold', threshold=0.1)
    assert all(spk_idx == arange(1, len(x), 4))

    xx = -x # edge case: first point > threshold
    spk_idx = detect_spikes(xx, method='derivative')
    assert all(spk_idx == arange(4, len(xx)-1, 4))

    spk_idx = detect_spikes(xx, method='threshold', threshold=0.1)
    assert all(spk_idx == arange(3, len(xx)-1, 4))


