import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.brian1 import Brian1Engine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLBrianEngine(JNeuroMLEngine):

    name = "jNeuroML_Brian"
    
    python3_compatible = Brian1Engine.python3_compatible

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLBrianEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and Brian1Engine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not Brian1Engine.is_installed(None):
            Brian1Engine.install(None)

        JNeuroMLBrianEngine.path = JNeuroMLEngine.path + \
            ":" + Brian1Engine.path
        JNeuroMLBrianEngine.environment_vars = {}
        JNeuroMLBrianEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLBrianEngine.environment_vars.update(
            Brian1Engine.environment_vars)
        inform("PATH: " + JNeuroMLBrianEngine.path)
        inform("Env vars: %s" % JNeuroMLBrianEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLBrianEngine.name), indent=1)
            
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            
            self.stdout = check_output([jnml, self.modelpath, '-brian'], cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            self.stdout += check_output(['python', self.modelpath.replace('.xml', '_brian.py'), '-nogui'], cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLBrianEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLBrianEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
