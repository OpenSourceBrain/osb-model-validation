import os
import subprocess as sp
import sys

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class PyLemsEngine(OMVEngine):
    
    name = "PyLEMS"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            import lems
            ret = 'v%s'%lems.__version__
            inform("PyLEMS %s is correctly installed..." % ret, indent=2, verbosity=2)

        except Exception as err:
            inform("Couldn't execute/import PyLEMS: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from omv.engines.getpylems import install_pylems
        home = os.environ['HOME']
        p = os.path.join(home, 'pylems')
        PyLemsEngine.path = p
        PyLemsEngine.environment_vars = {'PYLEMS_HOME': p}
        inform('Will fetch and install the latest PyLEMS', indent=2)
        install_pylems()
        inform('Done...', indent=2)
        
    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['pylems', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Process error with %s: "%self.name, err, indent=1)
            self.returncode = err.returncode
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"


















