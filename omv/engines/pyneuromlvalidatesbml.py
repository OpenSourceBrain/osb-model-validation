import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import EngineExecutionError
from omv.engines.pyneuroml_ import PyNeuroMLEngine
from omv.engines.engine import PATH_DELIMITER
from omv.engines.utils import resolve_paths


class PyNeuroMLValidateSBMLEngine(PyNeuroMLEngine):
    name = "pyNeuroML_validate_sbml"

    @staticmethod
    def is_installed():
        if not PyNeuroMLEngine.is_installed():
            return False

        ret = True
        try:
            inform(
                "Checking whether %s is installed..."
                % PyNeuroMLValidateSBMLEngine.name,
                indent=1,
                verbosity=2,
            )
            import libsbml

            ret = "v%s" % libsbml.__version__

        except Exception as err:
            inform(
                "Couldn't import %s into Python: " % PyNeuroMLValidateSBMLEngine.name,
                err,
                indent=1,
                verbosity=1,
            )
            ret = False
        return ret

    @staticmethod
    def install(version):
        if not PyNeuroMLEngine.is_installed():
            PyNeuroMLEngine.install(None)

        from omv.engines.getlibsbml import install_libsbml

        inform("Will fetch and install the latest libsbml", indent=2)
        install_libsbml(version)

    def run(self):
        try:
            path_s = resolve_paths(self.modelpath)

            inform(
                "Path [%s] expanded to: %s" % (self.modelpath, path_s),
                indent=1,
                verbosity=1,
            )

            # pynml = PyNeuroMLEngine.get_executable() #could implement more flexible way to find the executeable
            cmds = ["pynml", "-validate-sbml"]
            for p in path_s:
                cmds.append(p)

            inform(
                "Running with %s, using: %s..."
                % (PyNeuroMLValidateSBMLEngine.name, cmds),
                indent=1,
            )
            self.stdout = check_output(
                cmds,
                cwd=os.path.dirname(self.modelpath.split(PATH_DELIMITER)[0]),
                # env=PyNeuroMLEngine.get_environment(),
            )
            inform(
                "Success with running ",
                PyNeuroMLValidateSBMLEngine.name,
                indent=1,
                verbosity=1,
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform(
                "Error with ", PyNeuroMLValidateSBMLEngine.name, indent=1, verbosity=1
            )
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
