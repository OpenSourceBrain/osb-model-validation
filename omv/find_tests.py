from os import environ, getcwd
from pathlib import Path
from parse_omt import parse_omt
from common.inout import load_yaml, inform


def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if environ.get('TRAVIS'):
        engine = environ.get('OMV_ENGINE').lower()
        tallies = [parse_omt(t)
                   for t in all_omts
                   if load_yaml(t)['engine'].lower() == engine]
    else:
        tallies = [parse_omt(t) for t in all_omts]

    results = [t.all_passed() for t in tallies]
    inform('')
    inform("%i tests found" % len(all_omts),
           overline='-', underline='-', center=True)
    inform('')
    if all(results):
        inform("All tests passing!", underline='=', center=True)
    else:
        failed = [t.experiments for t in tallies if not t.all_passed()]
        inform("Some tests failed: ",  failed, underline='=')

    assert all(results)


def test_one(omt_fname):
    tally = parse_omt(omt_fname)
    inform('')
    if tally.all_passed():
        inform("Test passed: %s" % omt_fname, overline='=',
               center=True)
    else:
        inform("Test failed: %s %s" % (omt_fname, tally.omt),
               underline='=', center=True)

    assert(tally.all_passed())
