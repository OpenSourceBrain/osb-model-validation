import os
from glob import glob
import platform
import subprocess as sp
from textwrap import dedent
from utils.wdir import working_dir
from engine import OMVEngine, EngineExecutionError
from os.path import dirname

from ..common.inout import inform, is_verbose


class NeuronEngine(OMVEngine):

    name = "NEURON"

    def __init__(self, target, do_not_check_install=False, engine_version=None):
        super(NeuronEngine, self).__init__(target, do_not_check_install)
        try:
            self.stdout = self.compile_modfiles()
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)
            
            
    @staticmethod
    def get_nrn_environment():

        home = os.environ['HOME']
        arch = platform.machine()
        pp = os.path.join(home, 'local/lib/python/site-packages')
        path = os.path.join(home, 'neuron/nrn/', arch, 'bin')
        environment_vars = {'PYTHONPATH': pp,
                            'NEURON_HOME': os.path.join(home, 'neuron/nrn/', arch)}

        return environment_vars, path

    @classmethod
    def is_installed(cls, version):
        ret = True
        
        try:
            output = sp.check_output(['nrniv', '--version'])
            if is_verbose():
                inform('%s was already installed locally'%output.strip(), indent=2)
        except OSError:
            try:
                environment_vars, path = NeuronEngine.get_nrn_environment()
                
                inform('Testing NEURON with env: %s and path: %s'%(cls.environment_vars, cls.path), indent=2)
                output = sp.check_output([path+'/nrniv', '--version'])
                if is_verbose():
                    inform('%s was already installed (by OMV..?)'%output.strip(), indent=2)
            except OSError:
                    inform('NEURON not currently installed', indent=2)
                    ret = False
        return ret
 
    @classmethod
    def install(cls, engine_version):
        import getnrn
        
        cls.environment_vars, cls.path = NeuronEngine.get_nrn_environment()
        
        inform('Will fetch and install the latest NEURON version', indent=2)
        getnrn.install_neuron()


    def compile_modfiles(self):
        with working_dir(dirname(self.modelpath)):
            out = 0
            if len(glob('*.mod')) > 0:
                inform('Compiling modfiles', indent=1)
                out = sp.check_output(['nrnivmodl'])
                inform(out, indent=2)
        return out


    def run(self):
        
        self.environment_vars = NeuronEngine.get_nrn_environment()
        self.set_environment()
        self.set_path()
        
        with working_dir(dirname(self.modelpath)):
            
            inform("Running %s on %s..." % (self.name, self.modelpath),
                   indent=1)
            p = sp.Popen(['nrniv'],
                         stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            cmd = '''\
            load_file("noload.hoc")
            //cvode_active(1)
            load_file("%s")
            %s
            ''' % (self.modelpath, '\n'.join(self.extra_pars))
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
            
    def build_query_string(self, name, cmd):
        return '{{%s}{print "%s: ", %s}}' % (cmd, name, name)

    def query_area(self, secname):
        qname = 'area_%s' % secname
        qcmd = 'forsec "%s" {for (x,0) area_%s+=area(x)}' % (secname, secname)
        name = self.register_query(qname, qcmd)
        return name
            
    def query_temperature(self):
        return self.register_query('temperature', 'temperature=celsius')





