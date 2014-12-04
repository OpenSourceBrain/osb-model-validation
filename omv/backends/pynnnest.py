import os
import subprocess as sp

from nest import NestBackend
from pynn import PyNNBackend

from ..common.inout import inform, trim_path, check_output
from backend import BackendExecutionError


class PyNNNestBackend(PyNNBackend):
    
    name = "PyNN_Nest"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               PyNNNestBackend.name, indent=1)
        return PyNNBackend.is_installed(None) and NestBackend.is_installed(None)
        
    @staticmethod
    def install(version):
        if not NestBackend.is_installed(None):
            NestBackend.install(None)
            inform("%s installed Nest..." % PyNNNestBackend.name, indent=2, verbosity =1)
        if not PyNNBackend.is_installed(None):
            PyNNBackend.install(None)
            inform("%s installed PyNN..." % PyNNNestBackend.name, indent=2, verbosity =1)

        PyNNNestBackend.path = PyNNBackend.path + \
            ":" + NestBackend.path
        PyNNNestBackend.environment_vars = {}
        PyNNNestBackend.environment_vars.update(
            PyNNBackend.environment_vars)
        PyNNNestBackend.environment_vars.update(
            NestBackend.environment_vars)
        inform("PATH: " + PyNNNestBackend.path)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'nest'],
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
















