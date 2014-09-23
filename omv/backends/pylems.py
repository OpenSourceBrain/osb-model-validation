import os
import subprocess as sp

from ..common.inout import inform
from backend import OMVBackend, BackendExecutionError


class PyLemsBackend(OMVBackend):
    
    name = "PyLEMS"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['pylems', '-h'], stdout=FNULL)
        except OSError as err:
            inform("Couldn't execute pylems:", err, indent=1)
            ret = True
        return ret
        
    def install(self, version):
        from getpylems import install_pylems
        home = os.environ['HOME']
        p = os.path.join(home, 'pylems')
        self.path = p
        self.environment_vars = {'PYEMS_HOME': p}
        inform('Will fetch and install the latest PyLEMS', indent=2)
        install_pylems()
        inform('Done...', indent=2)
        
    def run(self):
        try:
            inform("Running file %s with %s" % (self.modelpath, self.name), indent=1)
            self.stdout = sp.check_output(['lems', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
        except Exception as err:
            inform("Another error with running %s:"%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"


















