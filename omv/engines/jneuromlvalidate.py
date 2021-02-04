import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine, EngineExecutionError
from omv.common.inout import inform, check_output

# Make explicit list from: '*.nml myfile.xml' etc.
def resolve_paths(path_s):
    
    if '*' in path_s:
        import glob
        if ' ' in path_s:
            all = []
            for p in path_s.split(' '):
                for g in glob.glob(p):
                    all.append(g)
            path_s = all
        else:
            path_s = glob.glob(path_s)
    
    return path_s

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
            path_s = resolve_paths(self.modelpath)
                
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            cmds = [jnml, '-validate']
            for p in path_s: cmds.append(p)
            
            inform("Running with %s, using %s..." % (JNeuroMLValidateEngine.name,
                   cmds),
                   indent=1)
            self.stdout = check_output(cmds,
                cwd=os.path.dirname(self.modelpath),
                env=JNeuroMLEngine.get_environment())
            inform("Success with running ", JNeuroMLValidateEngine.name,
                   indent=1, verbosity=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ",  JNeuroMLValidateEngine.name,
                   indent=1, verbosity=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
