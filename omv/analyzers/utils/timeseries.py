def detect_spikes(v, method='threshold', threshold=0.):
    from numpy import flatnonzero, bitwise_and, roll, diff, array

    extrema = array([])

    if method == 'threshold':
        extrema = flatnonzero(bitwise_and((v < threshold), (roll(v,-1) >= threshold)))

    elif method == 'derivative':
        # This should only work for noiseless cases!
        dx = diff(v)
        extrema = flatnonzero(bitwise_and((dx <= 0), (roll(dx,1) > 0)))
    else:
        print 'still need to implement fancier spike detectors...'
        #see for example scipy.signal.find_peaks_cwt 
    return extrema

def load_data_file(fname, columns=(0,1), header_lines=0):
    from numpy import loadtxt
    return loadtxt(fname, usecols=columns, skiprows=header_lines).T

def compare_arrays(arrays, tolerance):
    from numpy import allclose, array
    a1, a2 = array(arrays)
    #print a1, a2
    #print '#tol', tolerance
    return allclose(a1, a2, tolerance)


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
    t, v = ts
    spk_idx = detect_spikes(v, method, threshold)
    return t[spk_idx]


def spikes_from_datafile(path, columns=(0,1), header=0, method='threshold', threshold=0):
    t, v = load_data_file(path, columns, header)
    spk_idx = detect_spikes(v, method, threshold)
    return t[spk_idx]


def timeseries_from_file_node(fn):
    fname = fn['path']
    cols = fn.get('columns', (0,1))
    hdr = fn.get('header', 0)
    return load_data_file(fname, cols, hdr)

def resting_from_file_node(fn):
    from numpy import mean
    tv = timeseries_from_file_node(fn)
    av = fn.get('average last', 1)
    return mean(tv[1, -av:])


def test_detect_spikes():
    from numpy import array, all, arange
    x = array([-1, 0, 1, 0] * 10) 

    spk_idx = detect_spikes(x, method='derivative')
    assert all(spk_idx == arange(2,len(x),4))

    spk_idx = detect_spikes(x, method='threshold', threshold=0.1)
    assert all(spk_idx == arange(1,len(x),4))














