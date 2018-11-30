import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class PyNNEngine(OMVEngine):
    
    name = "PyNN"

    @staticmethod
    def is_installed(version):
        ret = True
        try:
            import pyNN
            if is_verbose():
                inform("pyNN version %s is correctly installed..." % pyNN.__version__, indent=2)
            ret = 'v%s'%pyNN.__version__
            
        except Exception as err:
            inform("Couldn't import pyNN into Python: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getpynn import install_pynn
        home = os.environ['HOME']
        inform('Will fetch and install the latest pyNN', indent=2)
        install_pynn()
        inform('Done, PyNN is correctly installed...', indent=2)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
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
















