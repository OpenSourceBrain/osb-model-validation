"""OpenSourceBrain Model Validation and Testing
============================================

  Usage:
    omv all [-V | --verbose]
    omv test <testMe.omt> [-V | --verbose]
    omv autogen [options]
    omv install <engine>
    omv list-engines
    omv validate-mep <mepfile>
    omv validate-omt <omtfile>
    omv travis-conda-setup
    omv (-h | --help)
    omv --version

  Options:
    -h --help     Show this screen.
    -d --dryrun   Generate dry-run tests only [default: False].
    -V --verbose  Display additional diagnosis messages [default: False].
    --version     Show version.
    -y            Auto-select default options (non-interactive mode)
"""
from docopt import docopt
from find_tests import test_all, test_one
from validation import validate_mep
from autogen import autogen
from engines import OMVEngines
from utilities.travis_conda import generate_evalstring


def main():
    arguments = docopt(__doc__, version='OpenSourceBrain Model Validation 0.0')

    if arguments['--verbose']:
        import common.inout
        common.inout.__VERBOSITY__ = 1

    if arguments['test']:
        try:
            test_one(arguments['<testMe.omt>'])
        except AssertionError:
            print("Failed due to non passing tests")
            exit(1)

    elif arguments['all']:
        try:
            test_all()
        except AssertionError:
            print("Failed due to non passing tests")
            exit(1)

    elif arguments['validate-mep']:
        validate_mep.validate(arguments['<mepfile>'])

    elif arguments['validate-omt']:
        print('OMT validation not implemented yet!')

    elif arguments['install']:
        be = arguments['<engine>']
        if be not in OMVEngine:
            print('Engine' + be + 'unknown!')
        else:
            print('Will install: %s'% arguments['<engine>'])
            print('Engine installation not implemented yet!')

    elif arguments['list-engines']:
        for be in OMVEngine.keys():
            print(be)

    elif arguments['autogen']:
        print('Automatically generating model validation files')
        dry = arguments['--dryrun']
        auto = arguments['-y']
        autogen(auto, dry)

    elif arguments['travis-conda-setup']:
        generate_evalstring()


if __name__ == '__main__':
    main()
