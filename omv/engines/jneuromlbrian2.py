import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.brian2_ import Brian2Engine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLBrian2Engine(JNeuroMLEngine):

    name = "jNeuroML_Brian2"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLBrian2Engine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and Brian2Engine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not Brian2Engine.is_installed(None):
            Brian2Engine.install(None)

        JNeuroMLBrian2Engine.path = JNeuroMLEngine.path + \
            ":" + Brian2Engine.path
        JNeuroMLBrian2Engine.environment_vars = {}
        JNeuroMLBrian2Engine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLBrian2Engine.environment_vars.update(
            Brian2Engine.environment_vars)
        inform("PATH: " + JNeuroMLBrian2Engine.path)
        inform("Env vars: %s" % JNeuroMLBrian2Engine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLBrian2Engine.name), indent=1)
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            self.stdout = check_output([jnml, self.modelpath, '-brian2'], cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            self.stdout += check_output(['python', self.modelpath.replace('.xml', '_brian2.py'), '-nogui'], cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLBrian2Engine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLBrian2Engine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
