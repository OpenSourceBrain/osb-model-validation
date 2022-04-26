import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError
from omv.engines.geteden import DEFAULT_VERSION

class EdenEngine(OMVEngine):

    name = "EDEN"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            import eden_simulator

            ver = 'v%s???'%DEFAULT_VERSION #'v%s'%eden_simulator.__version__
            inform("EDEN version %s is correctly installed..." % ver, indent=2, verbosity=2)

            ret = ver

        except Exception as err:
            inform("Couldn't import EDEN into Python: ", err, indent=1, verbosity=1)
            ret = False
        return ret

    @staticmethod
    def install(version):
        from omv.engines.geteden import install_eden
        home = os.environ['HOME']
        inform('Will fetch and install the latest EDEN', indent=2)
        install_eden(version)
        inform('Done...', indent=2)

    def run(self):
        try:
            inform("Running a file %s with the simulator %s" % (trim_path(self.modelpath), self.name), indent=1)

            self.stdout = check_output(['python', self.modelpath],
                                          cwd=os.path.dirname(self.modelpath))

            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
