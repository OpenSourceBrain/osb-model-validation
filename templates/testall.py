from sys import argv
from os import environ, getcwd
from pathlib import Path 
from osb_test.parse_ost import parse_ost, load_yaml

def test_all():
    cwd = Path(getcwd())
    all_omts = [p.as_posix() for p in cwd.glob('**/*.omt')]
    if environ.get('TRAVIS'):
        engine = environ.get('OST_ENGINE').lower()
        tsts = [all(parse_ost(t))
                for t in all_omts 
                if load_yaml(t)['engine'].lower() == engine]
    else:
        tsts= [all(parse_ost(t)) for t in all_omts]
    assert all(tsts)




















