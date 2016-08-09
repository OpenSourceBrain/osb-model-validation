
import subprocess as sp

from utils.wdir import working_dir
from os.path import dirname


from ..common.inout import inform, is_verbose
from engine import OMVEngine


class PyneuroConstruct(OMVEngine):
    
    name = "Py_neuroConstruct"

    @staticmethod
    def is_installed(version):
        
        # Check whether nC is installed by trying to run: nC.sh -version
        
        return False
        
        
    @staticmethod
    def install(version):

        from getneuroconstruct import install_neuroconstruct

        # Add install path (containing nC.sh) to PyneuroConstruct.path


    def run(self):
        
        # Run the python interface to nC on the model file by constructing & running a command like:
        # ['nC.sh', '-python', self.modelpath]
        
        self.returncode = -1 #  fail at present
















