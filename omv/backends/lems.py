import os
import subprocess as sp

from ..common.output import inform
from backend import OMVBackend

class LemsBackend(OMVBackend):

    def is_installed(self, version):
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['jnml', '-h'], stdout=FNULL)
        except OSError:
            ret = False
        return ret
        
    def install(self, version):
        from getjnml import install_jnml
        self.path = "$HOME/jnml/jNeuroMLJar"
        self.environment_vars = {'JNML_HOME':'$HOME/jnml/jNeuroMLJar'}
        inform('Will fetch and install the latest JNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            self.stdout = sp.check_output(['jnml', self.modelpath, '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output


















