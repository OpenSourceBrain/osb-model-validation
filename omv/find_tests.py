from os import environ, getcwd
from pathlib import Path
from omv.parse_omt import parse_omt
from common.io import load_yaml, inform


def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if environ.get('TRAVIS'):
        engine = environ.get('OMV_ENGINE').lower()
        tsts = [all(parse_omt(t))
                for t in all_omts
                if load_yaml(t)['engine'].lower() == engine]
    else:
        tsts = [all(parse_omt(t)) for t in all_omts]

    inform("%i tests found" % len(all_omts), overline='-', center=True)
    if all(tsts):
        inform("All tests passing!", underline='-', center=True)
    else:
        inform("Some tests failed: %s" % (tsts), underline='-')

    assert all(tsts)


def test_one(omt_fname):
    results = parse_omt(omt_fname)
    if all(results):
        inform("Test passed: %s" % omt_fname, overline='-',
               center=True)
    else:
        inform("Test failed: %s %s" % (omt_fname, results),
               underline='-', center=True)

    assert(all(results))
