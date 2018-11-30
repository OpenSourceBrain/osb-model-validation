import os
import subprocess as sp

from omv.engines.neuron_ import NeuronEngine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNNNRNEngine(PyNNEngine):
    
    name = "PyNN_NEURON"

    @staticmethod
    def is_installed(version):
        if is_verbose():
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
        
        pynn_loc = sp.check_output(['python -c "import pyNN,os; print(os.path.dirname(pyNN.__file__))"'], shell=True,stderr=sp.STDOUT).strip()
        pynn_mod_dir = '%s/neuron/nmodl/'%pynn_loc
        
        inform("Attempting to compile PyNN mod files for standard models in %s..."%pynn_mod_dir, indent=2, verbosity =1)
        
        print(check_output(['ls', pynn_mod_dir], cwd=pynn_mod_dir))
        
        environment_vars, path = NeuronEngine.get_nrn_environment()
        inform("Using NEURON with env %s at %s..."%(environment_vars, path), indent=2, verbosity =1)
        
        print(check_output([environment_vars['NEURON_HOME']+'/bin/nrnivmodl'], cwd=pynn_mod_dir))


    def run(self):
        
        
        try:
            self.stdout = NeuronEngine.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)
        
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
















