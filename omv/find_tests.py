from os import environ, getcwd
from pathlib import Path
from omv.parse_omt import parse_omt
from omv.common.inout import load_yaml, inform, trim_path, is_verbose
from omv.tally import TallyHolder


def test_all(do_not_run=False, only_this_engine=None, include_temp_tests=False, ignore_non_py3=False):
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if include_temp_tests:
        all_omts += [p.as_posix() for p in cwd.glob('**/*.omt_')]
    
    th = TallyHolder()
    if environ.get('TRAVIS'):
        if not environ.get('OMV_ENGINE'):
            tallies = [parse_omt(t, ignore_non_py3=ignore_non_py3) for t in all_omts]
        else:
            engine = environ.get('OMV_ENGINE').lower()
            engine_version=None
            if ':' in engine:
                ee = engine.split(':')
                engine = ee[0]
                engine_version = ee[1]
            tallies = [parse_omt(t, engine_version=engine_version, ignore_non_py3=ignore_non_py3)
                       for t in all_omts
                       if load_yaml(t)['engine'].lower() == engine]
    elif only_this_engine:
        
        inform('Only running tests for engine: %s'%only_this_engine)
        tallies = [parse_omt(t, ignore_non_py3=ignore_non_py3)
                   for t in all_omts
                   if load_yaml(t)['engine'].lower() == only_this_engine.lower()]
    else:
        tallies = []
        failed = 0
        for i in range(len(all_omts)):
            t = all_omts[i]
            inform('')
            tally = parse_omt(t, do_not_run, ignore_non_py3=ignore_non_py3)
            if not tally.all_passed(): failed+=1
            if not do_not_run:
                inform('')
                inform('')
                inform('      [ Test %i of %i complete - failed so far: %s ]'%(i+1,len(all_omts),failed))
            tallies.append(tally)
        
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
        
    else:
        engs ={}
        tot_tests = 0
        for t in tallies:
            if not t.engine in engs:
                engs[t.engine]=0
            engs[t.engine]+=1
            tot_tests+=1
        inform('')
        for e in sorted(engs):
            inform('  Engine %s has %s tests'%(e, engs[e]))
        inform('')
        inform('  %s OMV tests in total'%(tot_tests))
        inform('')
            


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
