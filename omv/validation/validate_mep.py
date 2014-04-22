#!/usr/bin/env python
import sys
from validate import OMVValidator
from pkg_resources import resource_filename

def main():
    try:
        mep_src = sys.argv[1]
    except:
        print 'usage: validate_mep document.mep'
        sys.exit(1)
    s = OMVValidator()
    print 'validating document againt mep schema: ', 
    schema = resource_filename('omv', 'schemata/mep.yaml')
    print s.validate(schema, mep_src)


if __name__ == '__main__':
    main()





















