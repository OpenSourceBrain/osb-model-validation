import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError


class OctaveEngine(OMVEngine):
    
    name = "Octave"
    

    @staticmethod
    def is_installed(version):
        ret = True
        
        try:
            print(check_output(['octave', '-v']))
        except OSError as err:
            inform("Couldn't execute Octave!", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getoctave import install_octave
        
        inform('Will fetch and install the latest Octave', indent=2)
        install_octave()
        inform('Done...', indent=2)
        
        
    def run(self):
        
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['octave', '--no-window-system', '--silent', self.modelpath],
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


















