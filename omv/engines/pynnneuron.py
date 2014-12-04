import os
import subprocess as sp

from neuron import NeuronEngine
from pynn import PyNNEngine

from ..common.inout import inform, trim_path, check_output
from engine import OMVEngine, EngineExecutionError


class PyNNNRNEngine(PyNNEngine):
    
    name = "PyNN_NEURON"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed correctly..." %
               PyNNNRNEngine.name, indent=1)
        installed = PyNNEngine.is_installed(None) and NeuronEngine.is_installed(None)
        
        return installed
        
    @staticmethod
    def install(version):
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(None)
            inform("%s installed NEURON..." % PyNNNRNEngine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed(None):
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNNRNEngine.name, indent=2, verbosity =1)

        PyNNNRNEngine.path = PyNNEngine.path + \
            ":" + NeuronEngine.path
        PyNNNRNEngine.environment_vars = {}
        PyNNNRNEngine.environment_vars.update(
            PyNNEngine.environment_vars)
        PyNNNRNEngine.environment_vars.update(
            NeuronEngine.environment_vars)
        inform("PATH: " + PyNNNRNEngine.path, indent=2, verbosity =1)
        inform("Env vars: %s" % PyNNNRNEngine.environment_vars, indent=2, verbosity =1)
        import pyNN
        pynn_mod_dir = os.path.dirname(pyNN.__file__)+'/neuron/nmodl/'
        inform("Attempting to compile PyNN mod files for standard models in %s..."%pynn_mod_dir, indent=2, verbosity =1)
        
        print check_output(['ls', pynn_mod_dir], cwd=pynn_mod_dir)
        
        print check_output([NeuronEngine.environment_vars['NEURON_HOME']+'/bin/nrnivmodl'], cwd=pynn_mod_dir)


    def run(self):
        try:
                                          
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'neuron'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
















