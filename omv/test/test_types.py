import glob
from os.path import splitext, basename, normpath

def _walk_testdir(root, validator):
    for f in glob.glob(root + '/test/*.yaml'):
        print('found test document', f)
        fname = splitext(basename(f))[0]
        try:
            target = fname[:fname.rindex('.')]
        except ValueError:
            target = fname

        schema_src = normpath(''.join([root, '/', target , '.yaml']))
        print('using schema', schema_src)
        assert validator.validate(schema_src, f)
        print('valid!\n')

def test_base():
    from ..validation.rx_validator import RXSchemaValidator as v
    _walk_testdir('../schemata/types/base', v())
        

def test_derived():
    from ..validation.validate import OMVValidator as o
    _walk_testdir('../schemata/types', o())



















