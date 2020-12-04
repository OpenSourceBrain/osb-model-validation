
import subprocess as sp
from textwrap import dedent
from omv.engines.utils.wdir import working_dir
from os.path import dirname
import sys

from omv.engines.neuron_ import NeuronEngine

from omv.common.inout import inform, is_verbose, check_output
from omv.engines.engine import EngineExecutionError


class PyNRNEngine(NeuronEngine):
    
    name = "PyNEURON"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            inform("Checking whether %s is installed..." % PyNRNEngine.name, indent=1, verbosity=2)
            
            ### Prints to stderr!!
            #ret_str = check_output(['python -c "import neuron; print(neuron.h.nrnversion())"'], shell=True, verbosity=2)
            import neuron
            ret_str = neuron.h.nrnversion()
            
            ret = 'v%s'%ret_str.split()[3]
            if is_verbose():
                inform("PyNEURON version %s is correctly installed..." % ret, indent=2)
                
            
        except Exception as err: 
            inform("Couldn't import NEURON into Python: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(version)    # interpret version as version of NEURON!
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
            if sys.version_info[0]==3:
                c = dedent(cmd).encode()
            else:
                c = dedent(cmd)
            stdout, stderr = p.communicate(c)
            # with open('/tmp/omv_test.nrn.stdout', 'w') as f:
            #     f.write(stdout)
            self.stdout = str(stdout.decode())
            self.stderr = str(stderr.decode())
            
            inform("OUT: %s"% self.stdout, verbosity=1, indent=2)
            inform("ERR: %s"% self.stderr, verbosity=1, indent=2)
            inform("returncode: [%s]"% p.returncode, verbosity=1, indent=2)

            self.returncode = p.returncode
            if self.returncode != 0:
                raise EngineExecutionError
















