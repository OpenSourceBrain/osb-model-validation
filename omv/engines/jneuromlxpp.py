import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.xpp import XppEngine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLXppEngine(JNeuroMLEngine):
    name = "jNeuroML_XPP"

    @staticmethod
    def is_installed():
        if is_verbose():
            inform(
                "Checking whether %s is installed..." % JNeuroMLXppEngine.name,
                indent=1,
            )
        return JNeuroMLEngine.is_installed() and XppEngine.is_installed()

    @staticmethod
    def install(xpp_version):
        if not JNeuroMLEngine.is_installed():
            JNeuroMLEngine.install(None)
        if not XppEngine.is_installed():
            XppEngine.install(xpp_version)


    def run(self):
        self.environment_vars = XppEngine.get_xpp_environment()
        self.set_environment()
        try:
            inform(
                "Running file %s with %s"
                % (trim_path(self.modelpath), JNeuroMLXppEngine.name),
                indent=1,
            )
            from omv.engines.jneuroml import JNeuroMLEngine

            jnml = JNeuroMLEngine.get_executable()
            self.stdout = check_output(
                [jnml, self.modelpath, "-xpp"],
                cwd=os.path.dirname(self.modelpath),
                env=JNeuroMLEngine.get_environment(),
            )
            
            self.stdout = check_output(
                [self.environment_vars["XPP_HOME"] + "/xppaut", self.modelpath.replace('.xml','.ode'), '-silent'],
                cwd=os.path.dirname(self.modelpath),
            )

            inform("Success with running ", JNeuroMLXppEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLXppEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
