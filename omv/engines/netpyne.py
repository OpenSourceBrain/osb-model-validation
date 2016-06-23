import os
import subprocess as sp

from neuron import NeuronEngine

from ..common.inout import inform, trim_path, check_output, is_verbose
from engine import OMVEngine, EngineExecutionError


class NetPyNEEngine(OMVEngine):
    
    name = "NetPyNE"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed correctly..." %
                   NetPyNEEngine.name, indent=1)
    
        ret = True
        try:
            import netpyne
            if is_verbose():
                inform("%s version %s is correctly installed..." % (NetPyNEEngine.name,netpyne.__version__), indent=2)
        except Exception as err:
            inform("Couldn't import netpyne into Python: ", err, indent=1)
            ret = False
            
        installed = ret and NeuronEngine.is_installed(None)
        
        return installed
        
    @staticmethod
    def install(version):
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(None)
            inform("%s installed NEURON..." % NetPyNEEngine.name, indent=2, verbosity =1)
            
            
        from getnetpyne import install_netpyne
        home = os.environ['HOME']
        inform('Will fetch and install the latest NetPyNE', indent=2)
        install_netpyne()
        inform('Done, NetPyNE is correctly installed...', indent=2)

        NetPyNEEngine.path = NeuronEngine.path
        NetPyNEEngine.environment_vars = {}
        NetPyNEEngine.environment_vars.update(
            NeuronEngine.environment_vars)
            
        inform("PATH: " + NetPyNEEngine.path, indent=2, verbosity =1)
        inform("Env vars: %s" % NetPyNEEngine.environment_vars, indent=2, verbosity =1)
        '''
        import pyNN
        pynn_mod_dir = os.path.dirname(pyNN.__file__)+'/neuron/nmodl/'
        inform("Attempting to compile PyNN mod files for standard models in %s..."%pynn_mod_dir, indent=2, verbosity =1)
        
        print check_output(['ls', pynn_mod_dir], cwd=pynn_mod_dir)'''
        
        environment_vars, path = NeuronEngine.get_nrn_environment()
        inform("Using NEURON with env %s at %s..."%(environment_vars, path), indent=2, verbosity =1)
        
        #print check_output([environment_vars['NEURON_HOME']+'/bin/nrnivmodl'], cwd=pynn_mod_dir)


    def run(self):
        
        
        try:
            self.stdout = NeuronEngine.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)
        
        try:            
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, '-nogui'],
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
















