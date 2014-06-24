import os
import subprocess as sp

from ..common.output import inform
from jneuroml import JNeuroMLBackend

class JNeuroMLNRNBackend(JNeuroMLBackend):

    backend_name = "jNeuroML_NEURON"

    def run(self):
        try:
            self.stdout = sp.check_output(['jnml', self.modelpath, '-neuron', '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            


















