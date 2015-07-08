import os
import subprocess as sp

from ..common.inout import inform, trim_path
from engine import OMVEngine, EngineExecutionError


class JNeuroMLEngine(OMVEngine):

    name = "jNeuroML"
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['jnml' if os.name != 'nt' else 'jnml.bat', '-h'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getjnml import install_jnml
        home = os.environ['HOME']
        p = os.path.join(home, 'jnml/jNeuroMLJar')
        JNeuroMLEngine.path = p
        JNeuroMLEngine.environment_vars = {'JNML_HOME': p}
        inform('Will fetch and install the latest jNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name),
                   indent=1)
            self.stdout = sp.check_output(['jnml' if os.name != 'nt' else 'jnml.bat', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
