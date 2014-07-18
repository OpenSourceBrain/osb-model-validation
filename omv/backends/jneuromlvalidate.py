import os
import subprocess as sp

from jneuroml import JNeuroMLBackend

class JNeuroMLValidateBackend(JNeuroMLBackend):

    name = "jNeuroML_validate"

    @staticmethod
    def is_installed(version):
        print("Checking whether %s is installed..."%JNeuroMLValidateBackend.name)
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
            print("Running with %s..."%JNeuroMLValidateBackend.name)
            self.stdout = sp.check_output(['jnml', '-validate', self.modelpath], cwd=os.path.dirname(self.modelpath))
            print("Success with running %s..."%JNeuroMLValidateBackend.name)
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            


















