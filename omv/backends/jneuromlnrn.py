import os
import subprocess as sp

from jneuroml import JNeuroMLBackend
from neuron import NeuronBackend
from ..common.io import inform


class JNeuroMLNRNBackend(JNeuroMLBackend):

    name = "jNeuroML_NEURON"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               JNeuroMLNRNBackend.name, indent=1)
        return JNeuroMLBackend.is_installed(None) and NeuronBackend.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLBackend.is_installed(None):
            JNeuroMLBackend.install(None)
        if not NeuronBackend.is_installed(None):
            NeuronBackend.install(None)

        JNeuroMLNRNBackend.path = JNeuroMLBackend.path + \
            ":" + NeuronBackend.path
        JNeuroMLNRNBackend.environment_vars = {}
        JNeuroMLNRNBackend.environment_vars.update(
            JNeuroMLBackend.environment_vars)
        JNeuroMLNRNBackend.environment_vars.update(
            NeuronBackend.environment_vars)
        inform("PATH: " + JNeuroMLNRNBackend.path)
        inform("Env vars: %s" % JNeuroMLNRNBackend.environment_vars)

    def run(self):
        try:
            inform("Running with %s..." % JNeuroMLNRNBackend.name, indent=1)
            self.stdout = sp.check_output(['jnml', self.modelpath, '-neuron', '-nogui', '-run'],
                                          cwd=os.path.dirname(self.modelpath))
            inform("Success with running %s..." %
                   JNeuroMLNRNBackend.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with", JNeuroMLNRNBackend.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
