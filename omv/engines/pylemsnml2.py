import os
import subprocess as sp

from omv.engines.pylems import PyLemsEngine
from omv.engines.getnml2 import default_nml2_dir, install_nml2

from omv.common.inout import inform, trim_path, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class PyLemsNeuroML2Engine(OMVEngine):
    
    name = "PyLEMS_NeuroML2"


    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
                   PyLemsNeuroML2Engine.name, indent=1)
               
        nml2_installed = os.path.isdir(default_nml2_dir)
               
        if nml2_installed and PyLemsEngine.is_installed(None):
            return PyLemsEngine.is_installed(None)
        else:
            return False
        
    def install(self, version):
        
        if not PyLemsEngine.is_installed(None):
            PyLemsEngine.install(None)
        if not os.path.isdir(default_nml2_dir):
            install_nml2()
            
        inform('Finished installation of %s...'%self.name, indent=2)
        
    def run(self):
        try:
            nml2_comp_type_def_dir = os.path.join(default_nml2_dir,'NeuroML2CoreTypes')
            
            inform("Running file %s with %s, including path: %s" % (trim_path(self.modelpath), self.name, nml2_comp_type_def_dir), indent=1)
            
            self.stdout = sp.check_output(['pylems', '-I', nml2_comp_type_def_dir, self.modelpath, '-nogui'],
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


















