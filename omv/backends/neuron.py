import os
from glob import glob
import platform
import subprocess as sp
from textwrap import dedent
from utils.wdir import working_dir
from backend import OMVBackend
from os.path import dirname

from ..common.output import inform

class NeuronBackend(OMVBackend):


    def __init__(self, target):
        super(NeuronBackend, self).__init__(target)
        try:
            self.stdout = self.compile_modfiles()
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)

    def is_installed(self, version):

        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['nrniv', '--version'], stdout=FNULL)
        except OSError:
            ret =  False
        return ret
 

    def install(self, backend_version):
        import getnrn
        home = os.environ['HOME']
        arch = platform.machine()
        self.path = "%/neuron/nrn/`arch`/bin" % (home, arch)
        self.environment_vars = {'PYTHONPATH':'$PYTHONPATH:$HOME/local/lib/python/site-packages'}
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
        with working_dir(dirname(self.modelpath)):
            p = sp.Popen(['nrniv'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            cmd = '''\
            load_file("noload.hoc")
            cvode_active(1)
            load_file("%s")
            %s
            ''' % (self.modelpath, '\n'.join(self.extra_pars))
            stdout, stderr = p.communicate(dedent(cmd))
            with open('/tmp/omv_test.nrn.stdout', 'w') as f:
                f.write(stdout)
            self.stdout = stdout
            self.stderr = stderr
            self.returncode = p.returncode

    def register_query(self, name, cmd=''):
        query = '{{%s}{print "%s: ", %s}}' % (cmd, name, name)
        inform('registered nrn query:', query, indent=2)
        self.extra_pars.append(query)
        return name

    def fetch_query(self, key):
        import re
        m = re.search(key+':'+'\s*([0-9]*\.?[0-9]+)\s*', self.stdout)
        if m:
            return m.groups()[0]
        else:
            print 'not found!'
            raise KeyError

    def query_area(self, secname):
        name = self.register_query('area_%s'%secname, 'forsec "%s" {for (x,0) area_%s+=area(x)}'%(secname,secname))
        return name
            
    def query_temperature(self):
        return self.register_query('temperature', 'temperature=celsius')





