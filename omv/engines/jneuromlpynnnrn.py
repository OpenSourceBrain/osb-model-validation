import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.pynnneuron import PyNNNRNEngine
from omv.engines.neuron_ import NeuronEngine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLPyNNNRNEngine(JNeuroMLEngine):

    name = "jNeuroML_PyNN_NEURON"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLPyNNNRNEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and PyNNNRNEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
            inform("%s installed JNeuroML..." % JNeuroMLPyNNNRNEngine.name, indent=2, verbosity =1)
        if not PyNNNRNEngine.is_installed(None):
            PyNNNRNEngine.install(None)
            inform("%s installed PyNN & NRN..." % JNeuroMLPyNNNRNEngine.name, indent=2, verbosity =1)
            
        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()

        JNeuroMLPyNNNRNEngine.path = JNeuroMLEngine.path+":"+path_nrn
        JNeuroMLPyNNNRNEngine.environment_vars = {}
        JNeuroMLPyNNNRNEngine.environment_vars.update(JNeuroMLEngine.environment_vars)
        JNeuroMLPyNNNRNEngine.environment_vars.update(PyNNEngine.environment_vars)
        JNeuroMLPyNNNRNEngine.environment_vars.update(environment_vars_nrn)
        inform("PATH: " + JNeuroMLPyNNNRNEngine.path)
        inform("Env vars: %s" % JNeuroMLPyNNNRNEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLPyNNNRNEngine.name), indent=1)
            
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            
            self.stdout = check_output(
                [jnml, self.modelpath, '-pynn', '-run-neuron'],
                cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            inform("Success with running ",
                   JNeuroMLPyNNNRNEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLPyNNNRNEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
