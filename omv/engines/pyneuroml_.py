import os
import subprocess as sp

from omv.common.inout import inform, trim_path, is_verbose, check_output as co
from engine import OMVEngine, EngineExecutionError


class PyNeuroMLEngine(OMVEngine):

    name = "pyNeuroML"
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            if is_verbose():
                inform("Checking whether %s is installed..." %
                   PyNeuroMLEngine.name, indent=1)
            FNULL = open(os.devnull, 'w')
            sp.check_call(['pynml' if os.name != 'nt' else 'pynml.bat', '-h'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getpyneuroml import install_pynml
        inform('Will fetch and install the latest pyNeuroML', indent=2)
        install_pynml()

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name),
                   indent=1)
            self.stdout = co(['pynml' if os.name != 'nt' else 'pynml.bat', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
