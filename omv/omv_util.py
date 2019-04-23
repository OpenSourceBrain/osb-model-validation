"""OpenSourceBrain Model Validation and Testing
============================================

  Usage:
    omv all [-V | --verbose] [--engine=engine]
    omv all_ [-V | --verbose] [--engine=engine]
    omv test <testMe.omt> [-V | --verbose]
    omv autogen [options]
    omv install <engine>
    omv find
    omv (list-engines | list)
    omv validate-mep <mepfile>
    omv validate-omt <omtfile>
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
from omv.find_tests import test_all, test_one
from omv.validation import validate_mep
from omv.autogen import autogen
from omv.engines import OMVEngines
from omv.common.inout import inform
import os

from omv.common.inout import set_verbosity


def main():
    arguments = docopt(__doc__, version='OpenSourceBrain Model Validation 0.1.3')
    set_env_vars()

    if arguments['--verbose']:
        set_verbosity(1)

    if arguments['test']:
        try:
            test_one(arguments['<testMe.omt>'])
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    elif arguments['all']:
        try:
            test_all(only_this_engine=arguments['--engine'])
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    # Includes *.omt_, i.e. temporary test files
    elif arguments['all_']:
        try:
            test_all(only_this_engine=arguments['--engine'],include_temp_tests=True)
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)
            
    elif arguments['find']:
        try:
            test_all(do_not_run=True)
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    elif arguments['validate-mep']:
        validate_mep.validate(arguments['<mepfile>'])

    elif arguments['validate-omt']:
        inform('OMT validation not implemented yet!')
        exit(1)

    elif arguments['install']:
        set_verbosity(1)
        eng = arguments['<engine>']
        engine_version=None
        
        if ':' in eng:
            ee = eng.split(':')
            eng = ee[0]
            engine_version = ee[1]
            inform('Engine %s version %s will be used...'%(eng, engine_version))
            
        if eng.lower() not in [e.lower() for e in OMVEngines]:
            inform('Engine ' + eng + ' unknown!')
        else:
            
            inform('Trying to install: %s'% eng)
            already_installed = False
            
            if eng.lower() == 'NEURON'.lower():
                from engines.neuron_ import NeuronEngine
                if not NeuronEngine.is_installed(''):
                    from engines.getnrn import install_neuron
                    install_neuron()
                else:
                    already_installed = True
                    
            elif eng.lower() == 'PyNEURON'.lower():
                from engines.pyneuron import PyNRNEngine
                if not PyNRNEngine.is_installed(''):
                    from engines.getnrn import install_neuron
                    install_neuron()
                else:
                    already_installed = True
                    
            elif eng.lower() == 'jLEMS'.lower():
                from engines.jlems import JLemsEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getjlems import install_jlems
                    install_jlems()
                    
            elif eng.lower() == 'jNeuroML'.lower():
                from engines.jneuroml import JNeuroMLEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getjnml import install_jnml
                    install_jnml()
                    
            elif eng.lower() == 'neuroConstruct' or eng == 'Py_neuroConstruct'.lower():
                from engines.pyneuroconstruct import PyneuroConstructEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getneuroconstruct import install_neuroconstruct
                    install_neuroconstruct()

            elif eng.lower() == 'pyNeuroML'.lower():
                from engines.pyneuroml_ import PyNeuroMLEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getpyneuroml import install_pynml
                    install_pynml()            
                    
            elif eng.lower() == 'PyLEMS_NeuroML2'.lower():
                from engines.getpylems import install_pylems
                install_pylems()
                from engines.getnml2 import install_nml2
                install_nml2()
            elif eng.lower() == 'genesis'.lower():
                from engines.getgenesis import install_genesis
                install_genesis()
            elif eng.lower() == 'Moose'.lower():
                from engines.getmoose import install_moose
                install_moose()
            elif eng.lower() == 'NetPyNE'.lower():
                from engines.getnetpyne import install_netpyne
                install_netpyne()
            elif eng.lower() == 'Brian'.lower():
                from engines.getbrian1 import install_brian
                install_brian()
            elif eng.lower() == 'Brian2'.lower():
                from engines.getbrian2 import install_brian2
                install_brian2(engine_version)
            elif eng.lower() == 'NEST'.lower():
                from engines.getnest import install_nest
                install_nest()
            elif eng.lower() == 'PyNN'.lower():
                from engines.getpynn import install_pynn
                install_pynn()
            else:
                inform('Code not implemented yet for installing %s using: omv install! Try running a test using this engine.'%eng)
                exit(1)
            if already_installed:
                inform('Engine %s was already installed'%eng)
                
                
            

    elif arguments['list-engines'] or arguments['list']:
        
        inform('OMV is checking which engines are currently installed...')
        
        engines = sorted(OMVEngines.keys())
        
        installed = {}
        for engine in engines:
            installed[engine] = OMVEngines[engine].is_installed('')
            
        inform('')
        inform('The following engines are currently supported by OMV:')
        inform('')
        for engine in engines:
            inform('  %s%s(installed: %s)'%(engine, ' '*(30-len(engine)), installed[engine]))
        inform('')

    elif arguments['autogen']:
        inform('Automatically generating model validation files')
        dry = arguments['--dryrun']
        auto = arguments['-y']
        autogen(auto, dry)

def set_env_vars():

    if os.name == 'nt':

        # Windows does not have a HOME var defined by default
        os.environ['HOME'] = os.environ['USERPROFILE']

if __name__ == '__main__':
    main()
