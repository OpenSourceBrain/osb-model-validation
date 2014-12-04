import os
import subprocess as sp

from jneuroml import JNeuroMLEngine, EngineExecutionError
from ..common.inout import inform


class JNeuroMLValidateEngine(JNeuroMLEngine):

    name = "jNeuroML_validate"

    @staticmethod
    def is_installed(version):
        return JNeuroMLEngine.is_installed(None)
    
    @staticmethod
    def install(version):
        
        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
    
        JNeuroMLValidateEngine.path = JNeuroMLEngine.path
        JNeuroMLValidateEngine.environment_vars = {}
        JNeuroMLValidateEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        
    def run(self):
        try:
            inform("Running with %s..." % JNeuroMLValidateEngine.name,
                   indent=1)
            self.stdout = sp.check_output(
                ['jnml', '-validate', self.modelpath],
                cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLValidateEngine.name,
                   indent=1, verbosity=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ",  JNeuroMLValidateEngine.name,
                   indent=1, verbosity=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
