import os
import subprocess as sp

from neuron import NeuronBackend
from pynn import PyNNBackend

from ..common.inout import inform, trim_path
from backend import OMVBackend, BackendExecutionError


class PyNNNRNBackend(PyNNBackend):
    
    name = "PyNN_NEURON"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               PyNNNRNBackend.name, indent=1)
        return PyNNBackend.is_installed(None) and NeuronBackend.is_installed(None)
        
    @staticmethod
    def install(version):
        if not NeuronBackend.is_installed(None):
            NeuronBackend.install(None)
        if not PyNNBackend.is_installed(None):
            PyNNBackend.install(None)

        PyNNNRNBackend.path = PyNNBackend.path + \
            ":" + NeuronBackend.path
        PyNNNRNBackend.environment_vars = {}
        PyNNNRNBackend.environment_vars.update(
            PyNNBackend.environment_vars)
        PyNNNRNBackend.environment_vars.update(
            NeuronBackend.environment_vars)
        inform("PATH: " + PyNNNRNBackend.path)
        inform("Env vars: %s" % PyNNNRNBackend.environment_vars)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = sp.check_output(['python', self.modelpath, 'neuron'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
















