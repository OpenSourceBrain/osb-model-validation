"""OpenSourceBrain Model Validation and Testing
============================================

  Usage:
    omv all  
    omv test <testMe.omt>
    omv validate-mep <mepfile>
    omv validate-omt <omtfile>
    omv install <backend> 
    omv list-backends 
    omv (-h | --help)
    omv --version
  
  Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --backends List known backends.
"""
from docopt import docopt
from find_tests import test_all, test_one
from validation import validate_mep
from backends import OMVBackends

def main():
    arguments = docopt(__doc__, version='OpenSourceBrain Model Validation 0.0')
    
    if arguments['test']:
        test_one(arguments['<testMe.omt>'])

    elif arguments['all']:
        test_all()

    elif arguments['validate-mep']:
        validate_mep.validate(arguments['<mepfile>'])

    elif arguments['validate-omt']:
        print 'OMT validation not implemented yet!'

    elif arguments['install']:
        be = arguments['<backend>']
        if be not in OMVBackends:
            print 'Backend', be, 'unknown!'
        else:
            print 'Will install', arguments['<backend>']
            print 'Backend installation not implemented yet!'
        
    elif arguments['list-backends']:
        for be in OMVBackends.keys():
            print be
        
    
    
if __name__ == '__main__':
    main()





















