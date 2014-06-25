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
    
    
    @staticmethod
    def install(version):
        
        if not JNeuroMLBackend.is_installed(None):
            JNeuroMLBackend.install(None)
        if not NeuronBackend.is_installed(None):
            NeuronBackend.install(None)
    
        JNeuroMLNRNBackend.path = JNeuroMLBackend.path+":"+NeuronBackend.path
        JNeuroMLNRNBackend.environment_vars = {}
        JNeuroMLNRNBackend.environment_vars.update(JNeuroMLBackend.environment_vars)
        JNeuroMLNRNBackend.environment_vars.update(NeuronBackend.environment_vars)
        print "PATH: "+JNeuroMLNRNBackend.path
        print JNeuroMLNRNBackend.environment_vars
        
        
    def run(self):
        try:
            print("Running with %s..."%JNeuroMLNRNBackend.name)
            self.stdout = sp.check_output(['jnml', self.modelpath, '-neuron', '-nogui', '-run'])
            print("Success with %s..."%JNeuroMLNRNBackend.name)
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            


















