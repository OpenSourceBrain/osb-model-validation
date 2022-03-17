import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError


class ArborEngine(OMVEngine):

    name = "Arbor"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            import arbor
            inform("Arbor version %s is correctly installed..." % arbor.__version__, indent=2, verbosity=2)

            ret = 'v%s'%arbor.__version__

        except Exception as err:
            inform("Couldn't import Arbor into Python: ", err, indent=1, verbosity=1)
            ret = False
        return ret

    @staticmethod
    def install(version):
        from omv.engines.getarbor import install_arbor
        home = os.environ['HOME']
        inform('Will fetch and install the latest Arbor', indent=2)
        install_arbor(version)
        inform('Done...', indent=2)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, '-nogui'],
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
