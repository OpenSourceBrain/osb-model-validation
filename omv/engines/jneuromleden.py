import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.eden_ import EdenEngine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLEdenEngine(JNeuroMLEngine):
    name = "jNeuroML_EDEN"

    @staticmethod
    def is_installed():
        if is_verbose():
            inform(
                "Checking whether %s is installed..." % JNeuroMLEdenEngine.name,
                indent=1,
            )
        return JNeuroMLEngine.is_installed() and EdenEngine.is_installed()

    @staticmethod
    def install(version):
        if not JNeuroMLEngine.is_installed():
            JNeuroMLEngine.install(None)
        if not EdenEngine.is_installed():
            EdenEngine.install(version)

        JNeuroMLEdenEngine.path = JNeuroMLEngine.path + ":" + EdenEngine.path
        JNeuroMLEdenEngine.environment_vars = {}
        JNeuroMLEdenEngine.environment_vars.update(JNeuroMLEngine.environment_vars)
        JNeuroMLEdenEngine.environment_vars.update(EdenEngine.environment_vars)
        inform("PATH: " + JNeuroMLEdenEngine.path)
        inform("Env vars: %s" % JNeuroMLEdenEngine.environment_vars)

    def run(self):
        try:
            inform(
                "Running file %s with %s"
                % (trim_path(self.modelpath), JNeuroMLEdenEngine.name),
                indent=1,
            )
            from omv.engines.jneuroml import JNeuroMLEngine

            jnml = JNeuroMLEngine.get_executable()
            self.stdout = check_output(
                [jnml, self.modelpath, "-eden"],
                cwd=os.path.dirname(self.modelpath),
                env=JNeuroMLEngine.get_environment(),
            )
            self.stdout += check_output(
                ["python", self.modelpath.replace(".xml", "_eden.py")],
                cwd=os.path.dirname(self.modelpath),
            )
            inform("Success with running ", JNeuroMLEdenEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLEdenEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
