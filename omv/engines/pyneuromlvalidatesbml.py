import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import EngineExecutionError
from omv.engines.pyneuroml_ import PyNeuroMLEngine 

class PyNeuroMLValidateSBMLEngine(PyNeuroMLEngine):
    name = "pyNeuroML_validate_sbml"

    @staticmethod
    def is_installed():
        if not PyNeuroMLEngine.is_installed(): return False

        ret = True
        try:
            inform(
                "Checking whether %s is installed..." % PyNeuroMLValidateSBMLEngine.name,
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
        if not PyNeuroMLEngine.is_installed(): PyNeuroMLEngine.install()

        from omv.engines.getlibsbml import install_libsbml

        inform("Will fetch and install the latest libsbml", indent=2)
        install_libsbml(version)

    def run(self):
        try:
            inform(
                "Running file %s with %s" % (trim_path(self.modelpath), self.name),
                indent=1,
            )
            self.stdout = check_output(
                ["pynml" if os.name != "nt" else "pynml.bat", "-validate-sbml", self.modelpath],
                cwd=os.path.dirname(self.modelpath),
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
