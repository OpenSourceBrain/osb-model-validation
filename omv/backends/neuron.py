import os
from glob import glob
import platform
import subprocess as sp
from textwrap import dedent
from utils.wdir import working_dir
from backend import OMVBackend
from os.path import dirname

from ..common.io import inform


class NeuronBackend(OMVBackend):

    name = "NEURON"

    def __init__(self, target):
        super(NeuronBackend, self).__init__(target)
        try:
            self.stdout = self.compile_modfiles()
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)

    @classmethod
    def is_installed(cls, version):
        inform("Checking whether %s is installed..." % cls.name,
               indent=1)

        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['nrniv', '--version'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
 
    @classmethod
    def install(cls, backend_version):
        import getnrn
        home = os.environ['HOME']
        arch = platform.machine()
        pp = os.path.join(home, 'local/lib/python/site-packages')
        cls.path = os.path.join(home, 'neuron/nrn/', arch, 'bin')
        cls.environment_vars = {'PYTHONPATH': pp,
                                'NEURON_HOME':os.path.join(home, 'neuron/nrn/', arch)}
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
        verbose = False
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
            with open('/tmp/omv_test.nrn.stdout', 'w') as f:
                f.write(stdout)
            self.stdout = stdout
            self.stderr = stderr
            
            if verbose:
                inform("OUT: ", stdout)
                inform("ERR: ", stderr)
                inform("returncode: ", p.returncode)

            self.returncode = p.returncode
            
    def build_query_string(self, name, cmd):
        return '{{%s}{print "%s: ", %s}}' % (cmd, name, name)

    def query_area(self, secname):
        qname = 'area_%s' % secname
        qcmd = 'forsec "%s" {for (x,0) area_%s+=area(x)}' % (secname, secname)
        name = self.register_query(qname, qcmd)
        return name
            
    def query_temperature(self):
        return self.register_query('temperature', 'temperature=celsius')





