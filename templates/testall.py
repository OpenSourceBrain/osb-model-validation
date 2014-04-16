from sys import argv
from os import environ
from glob import glob
from osb_test.parse_ost import parse_ost, load_yaml

def test_all():
    if environ.get('TRAVIS'):
        engine = environ.get('OST_ENGINE').lower()
        tsts = [all(parse_ost(f))
                for f in glob('*.ost') 
                if load_yaml(f)['engine'].lower() == engine]
    else:
        tsts= [parse_ost(f) for f in glob('*.ost')]
    assert all(tsts)




















