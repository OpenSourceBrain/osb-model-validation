import os
import subprocess as sp

from jneuroml import JNeuroMLBackend
from ..common.output import inform

class JNeuroMLValidateV1Backend(JNeuroMLBackend):

    name = "jNeuroML_validatev1"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..."%JNeuroMLValidateV1Backend.name, indent=1)
        return JNeuroMLBackend.is_installed(None)
    
    
    @staticmethod
    def install(version):
        
        if not JNeuroMLBackend.is_installed(None):
            JNeuroMLBackend.install(None)
    
        JNeuroMLValidateV1Backend.path = JNeuroMLBackend.path
        JNeuroMLValidateV1Backend.environment_vars = {}
        JNeuroMLValidateV1Backend.environment_vars.update(JNeuroMLBackend.environment_vars)
        
        
    def run(self):
        try:
            inform("Running with %s..."%JNeuroMLValidateV1Backend.name, indent=1)
            self.stdout = sp.check_output(['jnml', '-validatev1', self.modelpath], cwd=os.path.dirname(self.modelpath))
            inform("Success with running %s..."%JNeuroMLValidateV1Backend.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            


















