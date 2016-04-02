
import subprocess as sp
from textwrap import dedent
from utils.wdir import working_dir
from os.path import dirname

from neuron import NeuronEngine

from ..common.inout import inform, is_verbose
from engine import EngineExecutionError


class PyNRNEngine(NeuronEngine):

    name = "PyNEURON"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed correctly..." %
                   PyNRNEngine.name, indent=1)
        installed = NeuronEngine.is_installed(None)

        return installed

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

    def build_query_string(self, name, cmd):
        return "h('" + super(PyNRNEngine, self).build_query_string(name, cmd) + "')"


    def run(self):

        try:
            self.stdout = self.compile_modfiles()
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)

        with working_dir(dirname(self.modelpath)):

            inform("Running %s on %s..." % (self.name, self.modelpath),
                   indent=1)
            p = sp.Popen(['nrniv', '-python', self.modelpath, '-nogui'],
                         stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            stdout, stderr = p.communicate(dedent('\n'.join(self.extra_pars)))
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



