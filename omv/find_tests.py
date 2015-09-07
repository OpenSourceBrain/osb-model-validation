from os import environ, getcwd
from pathlib import Path
from parse_omt import parse_omt
from common.inout import load_yaml, inform, trim_path, is_verbose
from tally import TallyHolder


def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    th = TallyHolder()
    if environ.get('TRAVIS'):
        if not environ.get('OMV_ENGINE'):
            tallies = [parse_omt(t) for t in all_omts]
        else:
            engine = environ.get('OMV_ENGINE').lower()
            tallies = [parse_omt(t)
                       for t in all_omts
                       if load_yaml(t)['engine'].lower() == engine]
    else:
        tallies = [parse_omt(t) for t in all_omts]
        
    for t in tallies:
        th.add(t)

    results = [t.all_passed() for t in tallies]
    inform('')
    inform("%i test(s) run" % len(tallies),
           overline='-', underline='-', center=True)
    inform('')
    if all(results):
        inform("All tests passing!", underline='=', center=True)
    else:
        failed = [trim_path(t.omt) for t in tallies if not t.all_passed()]
        inform("Some test(s) failed: ",  failed, underline='=')
    
    if is_verbose():
        print('\n'+th.summary()+'\n')

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
