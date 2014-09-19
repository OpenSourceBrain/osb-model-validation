import os
import subprocess as sp

from ..common.inout import inform
from backend import OMVBackend, BackendExecutionError


class JNeuroMLBackend(OMVBackend):

    name = "jNeuroML"
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['jnml', '-h'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getjnml import install_jnml
        home = os.environ['HOME']
        p = os.path.join(home, 'jnml/jNeuroMLJar')
        JNeuroMLBackend.path = p
        JNeuroMLBackend.environment_vars = {'JNML_HOME': p}
        inform('Will fetch and install the latest jNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            inform("Running file %s with %s" % (self.modelpath, self.name),
                   indent=1)
            self.stdout = sp.check_output(['jnml', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
