import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.netpyne_ import NetPyNEEngine
from omv.engines.neuron_ import NeuronEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLNetPyNEEngine(JNeuroMLEngine):

    name = "jNeuroML_NetPyNE"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLNetPyNEEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and NetPyNEEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
            inform("%s installed JNeuroML..." % JNeuroMLNetPyNEEngine.name, indent=2, verbosity =1)
        if not NetPyNEEngine.is_installed(None):
            NetPyNEEngine.install(None)
            inform("%s installed NetPyNE (& NEURON)..." % JNeuroMLNetPyNEEngine.name, indent=2, verbosity =1)
            
        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()

        JNeuroMLNetPyNEEngine.path = JNeuroMLEngine.path+":"+path_nrn
        JNeuroMLNetPyNEEngine.environment_vars = {}
        JNeuroMLNetPyNEEngine.environment_vars.update(JNeuroMLEngine.environment_vars)
        JNeuroMLNetPyNEEngine.environment_vars.update(NetPyNEEngine.environment_vars)
        JNeuroMLNetPyNEEngine.environment_vars.update(environment_vars_nrn)
        inform("PATH: " + JNeuroMLNetPyNEEngine.path)
        inform("Env vars: %s" % JNeuroMLNetPyNEEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLNetPyNEEngine.name), indent=1)
            
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            self.stdout = check_output(
                [jnml, self.modelpath, '-netpyne', '-nogui', '-run'],
                cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            inform("Success with running ",
                   JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
