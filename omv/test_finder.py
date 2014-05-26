from sys import argv, exit
from os import environ, getcwd
from pathlib import Path 
from omv.parse_omt import parse_omt, load_yaml

def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if environ.get('TRAVIS'):
        engine = environ.get('OST_ENGINE').lower()
        tsts = [all(parse_omt(t))
                for t in all_omts 
                if load_yaml(t)['engine'].lower() == engine]
    else:
        tsts= [all(parse_omt(t)) for t in all_omts]
    assert all(tsts)

    print """

    --------------------------
     OMV: All tests passing! 
    --------------------------

    """
    
def test_one():
    try: 
        t = argv[1]
    except:
        exit('No omt file specified')
    assert(all(parse_omt(t)))




















