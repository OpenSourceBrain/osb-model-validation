import os
import subprocess as sp

from ..common.inout import inform, trim_path
from engine import OMVEngine, EngineExecutionError


class JLemsEngine(OMVEngine):
    
    name = "jLEMS"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['lems', '-h'], stdout=FNULL)
        except OSError as err:
            inform("Couldn't execute lems:", err, indent=1)
            ret = False
        return ret
        
    def install(self, version):
        from getjlems import install_jlems
        home = os.environ['HOME']
        p = os.path.join(home, 'jLEMS')
        self.path = p
        self.environment_vars = {'LEMS_HOME': p}
        inform('Will fetch and install the latest jLEMS', indent=2)
        install_jlems()
        inform('Done...', indent=2)
        
    def run(self):
        try:
            inform("Running file %s with jLEMS" % trim_path(self.modelpath), indent=1)
            self.stdout = sp.check_output(['lems', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running jLEMS:", err, indent=1)
            self.returncode = -1
            self.stdout = "???"


















