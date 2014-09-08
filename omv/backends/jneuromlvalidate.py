import os
import subprocess as sp

from jneuroml import JNeuroMLBackend
from ..common.output import inform

class JNeuroMLValidateBackend(JNeuroMLBackend):

    name = "jNeuroML_validate"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..."%JNeuroMLValidateBackend.name, indent=1)
        return JNeuroMLBackend.is_installed(None)
    
    
    @staticmethod
    def install(version):
        
        if not JNeuroMLBackend.is_installed(None):
            JNeuroMLBackend.install(None)
    
        JNeuroMLValidateBackend.path = JNeuroMLBackend.path
        JNeuroMLValidateBackend.environment_vars = {}
        JNeuroMLValidateBackend.environment_vars.update(JNeuroMLBackend.environment_vars)
        
        
    def run(self):
        try:
            inform("Running with %s..."%JNeuroMLValidateBackend.name, indent=1)
            self.stdout = sp.check_output(['jnml', '-validate', self.modelpath], cwd=os.path.dirname(self.modelpath))
            inform("Success with running %s..."%JNeuroMLValidateBackend.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with %s..."%JNeuroMLValidateBackend.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            


















