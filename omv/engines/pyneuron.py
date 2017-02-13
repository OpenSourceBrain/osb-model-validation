
import subprocess as sp
from textwrap import dedent
from omv.engines.utils.wdir import working_dir
from os.path import dirname

from omv.engines.neuron_ import NeuronEngine

from omv.common.inout import inform, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNRNEngine(NeuronEngine):
    
    name = "PyNEURON"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            if is_verbose():
                inform("Checking whether %s is installed..." % PyNRNEngine.name, indent=1)
            import neuron
            if is_verbose():
                inform("PyNEURON version %s is correctly installed..." % neuron.sys.version, indent=2)
            
        except Exception as err:
            inform("Couldn't import NEURON into Python: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(None)
            inform("%s installed NEURON..." % PyNRNEngine.name, indent=2, verbosity =1)

        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()
        
        PyNRNEngine.path = path_nrn
        PyNRNEngine.environment_vars = {}
        PyNRNEngine.environment_vars.update(environment_vars_nrn)
            
        inform("PATH: " + PyNRNEngine.path, indent=2, verbosity =1)
        inform("Env vars: %s" % PyNRNEngine.environment_vars, indent=2, verbosity =1)
        


    def run(self):
        
        try:
            self.stdout = NeuronEngine.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)
            
        with working_dir(dirname(self.modelpath)):
            
            inform("Running %s on %s..." % (self.name, self.modelpath),
                   indent=1)
            p = sp.Popen(['nrniv', '-python', self.modelpath, '-nogui'],
                         stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            cmd = '''\
            %s
            ''' % ('\n'.join(self.extra_pars))
            stdout, stderr = p.communicate(dedent(cmd))
            # with open('/tmp/omv_test.nrn.stdout', 'w') as f:
            #     f.write(stdout)
            self.stdout = stdout
            self.stderr = stderr
            
            inform("OUT: ", stdout, verbosity=1, indent=2)
            inform("ERR: ", stderr, verbosity=1, indent=2)
            inform("returncode: ", p.returncode, verbosity=1, indent=2)

            self.returncode = p.returncode
            if self.returncode is not 0:
                raise EngineExecutionError
















