import os
import sys
from glob import glob
import platform
import subprocess as sp
from textwrap import dedent
from omv.engines.utils.wdir import working_dir
from omv.engines.engine import OMVEngine, EngineExecutionError
from os.path import dirname
from omv.common.inout import check_output, inform, is_verbose


class NeuronEngine(OMVEngine):

    name = "NEURON"

    def __init__(self, target, do_not_check_install=False, engine_version=None):
        super(NeuronEngine, self).__init__(target, do_not_check_install, engine_version)
        
        inform("Checking whether %s (v %s) is already installed..." % (self.name, engine_version),
                   indent=1, verbosity=1)
        if not self.is_installed(''):
            try:
                self.install(engine_version)
            except Exception as e:
                inform(e)
                raise(EngineInstallationError(e))
        
        self.environment_vars, self.path = NeuronEngine.get_nrn_environment()
        self.set_environment()
        self.set_path()
        
            
    @staticmethod
    def get_nrn_environment():

        home = os.environ['HOME']
        arch = platform.machine()
        pp = os.path.join(home, 'local/lib/python/site-packages')
        
        environment_vars = {'PYTHONPATH': pp}
        if not 'NEURON_HOME' in os.environ:
            environment_vars['NEURON_HOME'] = os.path.join(home, 'neuron/nrn/', arch)
            path = os.path.join(home, 'neuron/nrn/', arch, 'bin')
        else:
            environment_vars['NEURON_HOME'] = os.environ['NEURON_HOME']
            path = os.path.join(os.environ['NEURON_HOME'], 'bin')

        inform("NEURON environment vars: %s, PATH: %s" % (environment_vars, path),indent=1, verbosity=1)
        
        return environment_vars, path


    @staticmethod
    def is_installed(version):
        ret = True
        if is_verbose():
                inform("Checking whether %s is installed..." %
                   NeuronEngine.name, indent=1)
        try:
            output = check_output(['nrniv', '--version'],verbosity=2)
            if is_verbose():
                inform('%s is installed'%output.strip(), indent=2)
            ret = 'v%s'%output.split()[3]
        except OSError:
            try:
                environment_vars, path = NeuronEngine.get_nrn_environment()
                
                inform('Testing NEURON with env: %s and path: %s'%(environment_vars, path), indent=2)
                output = check_output([path+'/nrniv', '--version'])
                if is_verbose():
                    inform('%s was already installed (by OMV..?)'%output.strip(), indent=2)
                    
                ret = 'v%s'%output.split()[3]
            except OSError:
                    inform('NEURON not currently installed', indent=2)
                    ret = False
        return ret
 
    @classmethod
    def install(cls, version):
        from omv.engines.getnrn import install_neuron
        
        cls.environment_vars, cls.path = NeuronEngine.get_nrn_environment()
        
        inform('Will fetch and install the latest NEURON version', indent=2)
        install_neuron(version)


    @classmethod
    def compile_modfiles(cls, modelpath):
        with working_dir(dirname(modelpath)):
            out = 0
            if len(glob('*.mod')) > 0:
                environment_vars, path = NeuronEngine.get_nrn_environment()
                inform('Compiling all mod files in directory: %s'%dirname(modelpath), indent=1)
                out = check_output([path+'/nrnivmodl'])
                inform(out, indent=2)
            elif len(glob('modfiles/*.mod')) > 0:
                environment_vars, path = NeuronEngine.get_nrn_environment()
                mod_file_path = dirname(modelpath)+"/modfiles"
                inform('Compiling all mod files in directory: %s'%mod_file_path, indent=1)
                out = check_output([path+'/nrnivmodl','modfiles'])
                inform(out, indent=2)
            elif len(glob('mod_files/*.mod')) > 0:
                environment_vars, path = NeuronEngine.get_nrn_environment()
                mod_file_path = dirname(modelpath)+"/mod_files"
                inform('Compiling all mod files in directory: %s'%mod_file_path, indent=1)
                out = check_output([path+'/nrnivmodl','mod_files'])
                inform(out, indent=2)
        return out


    def run(self):
        
        try:
            self.stdout = self.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)
        
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
            
    def build_query_string(self, name, cmd):
        return '{{%s}{print "%s: ", %s}}' % (cmd, name, name)

    def query_area(self, secname):
        qname = 'area_%s' % secname
        qcmd = 'forsec "%s" {for (x,0) area_%s+=area(x)}' % (secname, secname)
        name = self.register_query(qname, qcmd)
        return name
            
    def query_temperature(self):
        return self.register_query('temperature', 'temperature=celsius')





