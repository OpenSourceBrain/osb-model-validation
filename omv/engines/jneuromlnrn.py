import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.neuron_ import NeuronEngine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLNRNEngine(JNeuroMLEngine):

    name = "jNeuroML_NEURON"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLNRNEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and NeuronEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(None)
            
        JNeuroMLNRNEngine.get_jnmlnrnenv()
            
    @staticmethod
    def get_jnmlnrnenv():
            
        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()

        JNeuroMLNRNEngine.path = JNeuroMLEngine.path + \
            ":" + path_nrn
        JNeuroMLNRNEngine.environment_vars = {}
        JNeuroMLNRNEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLNRNEngine.environment_vars.update(
            environment_vars_nrn)
            
        JNeuroMLNRNEngine.environment_vars.update(JNeuroMLEngine.get_environment())
        
        inform("PATH: " + JNeuroMLNRNEngine.path)
        inform("Env vars: %s" % JNeuroMLNRNEngine.environment_vars)
        del JNeuroMLNRNEngine.environment_vars['PYTHONPATH']
        
        return JNeuroMLNRNEngine.environment_vars


    def run(self):
        self.stdout, self.returncode = \
            JNeuroMLNRNEngine.run_using_jnmlnrn_env(JNeuroMLNRNEngine.name, 
                                                    self.modelpath,
                                                    ['-neuron', '-nogui', '-run'])
        
        if self.returncode!=0:
            raise EngineExecutionError
        
    @staticmethod
    def run_using_jnmlnrn_env(engine, modelpath, args):

        try:
            env = JNeuroMLNRNEngine.get_jnmlnrnenv()
            inform("Running file %s with %s, env: %s" % (trim_path(modelpath), engine, env), indent=1)
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            cmds = [jnml, modelpath]
            cmds.extend(args)
            stdout = check_output(
                cmds,
                cwd=os.path.dirname(modelpath),
                env=env)
                
            inform("Success with running ", engine, indent=1)
            returncode = 0
            return stdout, returncode
        except sp.CalledProcessError as err:
            inform("Error with ", engine, indent=1)
            returncode = err.returncode
            stdout = err.output
            return stdout, returncode
            
