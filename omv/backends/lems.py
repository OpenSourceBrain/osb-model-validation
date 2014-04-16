import os
from ..common.output import inform
import subprocess as sp

class LemsBackend(object):

    def __init__(self, target):
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['jnml', '-h'], stdout=FNULL)
        except OSError:
            from getjnml import install_jnml
            inform('Will fetch and install the latest JNeuroML jar', indent=2)
            install_jnml()
        self.modelpath = target

    def run(self):
        try:
            self.stdout = sp.check_output(['jnml', self.modelpath, '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output


















