import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.moose_ import MooseEngine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLMooseEngine(JNeuroMLEngine):

    name = "jNeuroML_Moose"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLMooseEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and MooseEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not MooseEngine.is_installed(None):
            MooseEngine.install(None)

        JNeuroMLMooseEngine.path = JNeuroMLEngine.path + \
            ":" + JNeuroMLMooseEngine.path
        JNeuroMLMooseEngine.environment_vars = {}
        JNeuroMLMooseEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLMooseEngine.environment_vars.update(
            MooseEngine.environment_vars)
        inform("PATH: " + JNeuroMLMooseEngine.path)
        inform("Env vars: %s" % JNeuroMLMooseEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLMooseEngine.name), indent=1)
            
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            
            self.stdout = check_output([jnml, self.modelpath, '-moose'], cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            self.stdout += check_output(['python', self.modelpath.replace('.xml', '_moose.py'), '-nogui'], cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLMooseEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLMooseEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
