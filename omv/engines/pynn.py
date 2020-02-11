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
            
            ret_str = sp.check_output(['python -c "import pyNN; print(pyNN.__version__)"'], shell=True,stderr=sp.STDOUT)
            ret = len(ret_str) > 0
            
            if isinstance(ret_str, bytes):
                ret_str = ret_str.decode('utf-8')
            
            ret = 'v%s'%ret_str.strip()
            if is_verbose():
                inform("pyNN %s is correctly installed..." % ret, indent=2, verbosity=2)
            
        except Exception as err:
            inform("Couldn't import pyNN into Python: ", err, indent=1, verbosity=2)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from omv.engines.getpynn import install_pynn
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
















