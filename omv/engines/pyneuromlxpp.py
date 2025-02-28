import os
import subprocess as sp

from omv.common.inout import inform, check_output
from omv.engines.engine import EngineExecutionError
from omv.engines.pyneuroml_ import PyNeuroMLEngine


class PyNeuroMLXppEngine(PyNeuroMLEngine):
    name = "pyNEURON_XPP_LEMS"

    @staticmethod
    def is_installed():
        pynml_ver = PyNeuroMLEngine.is_installed()
        if not pynml_ver:
            return False
        else:
            return pynml_ver

    @staticmethod
    def install(version):
        if not PyNeuroMLEngine.is_installed():
            PyNeuroMLEngine.install(version)

    def run(self):
        try:
            # pynml = PyNeuroMLEngine.get_executable() #could implement more flexible way to find the executeable
            cmds = ["pynml-xpp"]
            cmds.append(self.modelpath)
            cmds.append("-lems")
            cmds.append("-run")

            inform(
                "Running with %s, using: %s..." % (PyNeuroMLXppEngine.name, cmds),
                indent=1,
            )
            self.stdout = check_output(cmds, cwd=os.path.dirname(self.modelpath))
            inform(
                "Success with running ",
                PyNeuroMLXppEngine.name,
                indent=1,
                verbosity=1,
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", PyNeuroMLXppEngine.name, indent=1, verbosity=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
