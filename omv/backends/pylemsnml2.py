import os
import subprocess as sp

from pylems import PyLemsBackend
from getnml2 import default_nml2_dir, install_nml2

from ..common.inout import inform
from backend import OMVBackend, BackendExecutionError


class PyLemsNeuroML2Backend(OMVBackend):
    
    name = "PyLEMS_NeuroML2"


    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               PyLemsNeuroML2Backend.name, indent=1)
               
        nml2_installed = os.path.isdir(default_nml2_dir)
               
        return PyLemsBackend.is_installed(None) and nml2_installed
        
    def install(self, version):
        
        if not PyLemsBackend.is_installed(None):
            PyLemsBackend.install(None)
        if not os.path.isdir(default_nml2_dir):
            getnml2.install_nml2(None)
            
        inform('Finished installation of %s...'%self.name, indent=2)
        
    def run(self):
        try:
            nml2_comp_type_def_dir = os.path.join(default_nml2_dir,'NeuroML2CoreTypes')
            
            inform("Running file %s with %s, including path: %s" % (self.modelpath, self.name, nml2_comp_type_def_dir), indent=1)
            
            self.stdout = sp.check_output(['pylems', '-I', nml2_comp_type_def_dir, self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"


















