
from omv.common.inout import set_verbosity

from omv.analyzers.utils.timeseries import *

def test_rates():

    set_verbosity(2)

    tsNone = []
    tsA = [0.1]
    tsB = [0.1, 0.2]

    ts1 = [0.1,0.2,0.3,0.40]
    ts2 = [0.1,0.3,0.50]

    methods = [ISI_BASED_SPIKERATE_CALC, DURATION_BASED_SPIKERATE_CALC]

    for method in methods:

        opts = [tsNone, tsA, tsB, ts1, ts2, {'0':ts1}, {'0':ts1, '1':ts2}]
        exp = {}
        exp[ISI_BASED_SPIKERATE_CALC] = \
               [0,0,10,10,0,10,5]
        exp[DURATION_BASED_SPIKERATE_CALC] = \
               [0,4,8,8,4,8,6]
               
        for i in range(len(opts)):
            opt = opts[i]
            start_time = 0
            end_time = 0.25
            r = get_spike_rate(opt, method, start_time, end_time)
            inform(' > Rate in %s->%s (%s) for %s: %s\n'%(start_time, end_time, method, opt,r), indent=2)
            assert r==exp[method][i]

if __name__ == '__main__':

    test_rates()