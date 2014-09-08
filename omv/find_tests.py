from os import environ, getcwd
from pathlib import Path 
from omv.parse_omt import parse_omt, load_yaml

from common.output import inform

def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    tests_run = []
    if environ.get('TRAVIS'):
        engine = environ.get('OMV_ENGINE').lower()
        tsts = [all(parse_omt(t))
                for t in all_omts 
                if load_yaml(t)['engine'].lower() == engine]
    else:
        tsts= [all(parse_omt(t)) for t in all_omts]
        

    info = ""
    for omt in all_omts:
        info += omt + "\n" 
        
    inform("\n")
    inform("==================================")
    inform("%i tests found"%len(all_omts), indent=1)
    if all(tsts):
        inform("All tests passing!", indent=1)
    else:
        inform("Some tests failed: %s"%(tsts), indent=1)
    inform("==================================")
    
    assert all(tsts)
    
def test_one(omt_fname):
    results = parse_omt(omt_fname)
    inform("\n")
    inform("==================================")
    if all(results):
        inform("Test passed: %s"%omt_fname, indent=1)
    else:
        inform("Test failed: %s %s"%(omt_fname, results), indent=1)
    inform("==================================")
    
    assert(all(results))




















