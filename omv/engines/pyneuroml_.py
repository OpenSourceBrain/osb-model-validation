import os
import subprocess as sp

from omv.common.inout import inform, trim_path, is_verbose, check_output 
from omv.engines.engine import OMVEngine, EngineExecutionError


class PyNeuroMLEngine(OMVEngine):

    name = "pyNeuroML"
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            inform("Checking whether %s is installed..." % PyNeuroMLEngine.name, indent=1, verbosity=2)
            import pyneuroml
            ret = 'v%s'%pyneuroml.__version__
        
        except Exception as err:
            inform("Couldn't import %s into Python: "% PyNeuroMLEngine.name, err, indent=1, verbosity=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from omv.engines.getpyneuroml import install_pynml
        inform('Will fetch and install the latest pyNeuroML', indent=2)
        install_pynml()

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name),
                   indent=1)
            self.stdout = check_output(['pynml' if os.name != 'nt' else 'pynml.bat', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
