from os import environ, getcwd
from pathlib import Path
from omv.parse_omt import parse_omt
from omv.common.inout import load_yaml, inform, trim_path, is_verbose
from omv.tally import TallyHolder


def test_all(do_not_run=False, only_this_engine=None, include_temp_tests=False):
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if include_temp_tests:
        all_omts += [p.as_posix() for p in cwd.glob('**/*.omt_')]
    
    th = TallyHolder()
    if environ.get('TRAVIS'):
        if not environ.get('OMV_ENGINE'):
            tallies = [parse_omt(t) for t in all_omts]
        else:
            engine = environ.get('OMV_ENGINE').lower()
            tallies = [parse_omt(t)
                       for t in all_omts
                       if load_yaml(t)['engine'].lower() == engine]
    elif only_this_engine:
        
        inform('Only running tests for engine: %s'%only_this_engine)
        tallies = [parse_omt(t)
                   for t in all_omts
                   if load_yaml(t)['engine'].lower() == only_this_engine.lower()]
    else:
        tallies = []
        for i in range(len(all_omts)):
            t = all_omts[i]
            inform('')
            inform('  Test (%i/%i)'%(i+1,len(all_omts)))
            tallies.append(parse_omt(t, do_not_run))
        
    tallies.sort()
        
    if not do_not_run:
        for t in tallies:
            th.add(t)

        results = []
        for i in range(len(tallies)):
            t = tallies[i]
            results.append(t.all_passed())
        inform('')
        inform("%i test(s) run" % len(tallies),
               overline='-', underline='-', center=True)
        inform('')
        if len(results)==0:
            inform("No tests found!", underline='=', center=True)
        elif all(results):
            inform("All tests passing!", underline='=', center=True)
        else:
            failed = [trim_path(t.omt) for t in tallies if not t.all_passed()]
            inform("Some test(s) failed: ",  failed, underline='=')

        if is_verbose():
            print('\n'+th.summary()+'\n')

        assert len(results)>0
        assert all(results)


def test_one(omt_fname):
    tally = parse_omt(omt_fname)
    inform('')
    if tally.all_passed():
        inform("Test passed: %s" % omt_fname, overline='=',
               center=True)
    else:
        inform("Test failed: %s" % (omt_fname),
               underline='=', center=True)
               
    if is_verbose():
        th = TallyHolder()
        th.add(tally)
        print('\n'+th.summary()+'\n')

    assert(tally.all_passed())
