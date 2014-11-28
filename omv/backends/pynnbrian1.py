import os
import subprocess as sp

from brian1 import Brian1Backend
from pynn import PyNNBackend

from ..common.inout import inform, trim_path
from backend import OMVBackend, BackendExecutionError


class PyNNBrian1Backend(PyNNBackend):
    
    name = "PyNN_Brian1"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               PyNNBrian1Backend.name, indent=1)
        return PyNNBackend.is_installed(None) and Brian1Backend.is_installed(None)
        
    @staticmethod
    def install(version):
        if not PyNNBackend.is_installed(None):
            PyNNBackend.install(None)
        if not Brian1Backend.is_installed(None):
            Brian1Backend.install(None)

        PyNNBrian1Backend.path = PyNNBackend.path + \
            ":" + Brian1Backend.path
        PyNNBrian1Backend.environment_vars = {}
        PyNNBrian1Backend.environment_vars.update(
            PyNNBackend.environment_vars)
        PyNNBrian1Backend.environment_vars.update(
            Brian1Backend.environment_vars)
        inform("PATH: " + PyNNBrian1Backend.path)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = sp.check_output(['python', self.modelpath, 'brian'],
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
















