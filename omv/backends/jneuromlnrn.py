import os
import subprocess as sp

from ..common.output import inform
from jneuroml import JNeuroMLBackend
from neuron import NeuronBackend

class JNeuroMLNRNBackend(JNeuroMLBackend):

    name = "jNeuroML_NEURON"

    @staticmethod
    def is_installed(version):
        print("Checking whether %s is installed..."%JNeuroMLNRNBackend.name)
        return JNeuroMLBackend.is_installed(None) and NeuronBackend.is_installed(None)
    
    
    def install(self, version):
        from getjnml import install_jnml
        home = os.environ['HOME']
        p = os.path.join(home, 'jnml/jNeuroMLJar')
        self.path = p
        self.environment_vars = {'JNML_HOME': p}
        inform('Will fetch and install the latest jNeuroML jar for '+self.name, indent=2)
        install_jnml()
        
    def run(self):
        try:
            self.stdout = sp.check_output(['jnml', self.modelpath, '-neuron', '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            


















