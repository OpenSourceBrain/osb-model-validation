import os
import subprocess as sp

from jneuroml import JNeuroMLEngine, EngineExecutionError
from jneuromlvalidate import resolve_paths

from ..common.inout import inform


class JNeuroMLValidateV1Engine(JNeuroMLEngine):

    name = "jNeuroML_validatev1"

    @staticmethod
    def is_installed(version):
        return JNeuroMLEngine.is_installed(None)
    
    @staticmethod
    def install(version):
        
        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
    
        JNeuroMLValidateV1Engine.path = JNeuroMLEngine.path
        JNeuroMLValidateV1Engine.environment_vars = {}
        JNeuroMLValidateV1Engine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        
    def run(self):
        try:
            path_s = resolve_paths(self.modelpath)
                
            cmds = ['jnml' if os.name != 'nt' else 'jnml.bat', '-validatev1']
            for p in path_s: cmds.append(p)
            
            inform("Running with %s, using %s..." % (JNeuroMLValidateV1Engine.name,
                   cmds),
                   indent=1)
            self.stdout = sp.check_output(cmds,
                cwd=os.path.dirname(self.modelpath))
            inform("Success with running ",  JNeuroMLValidateV1Engine.name,
                   indent=1, verbosity=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
            


















