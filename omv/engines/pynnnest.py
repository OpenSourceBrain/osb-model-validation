import os
import subprocess as sp

from nest import NestEngine
from pynn import PyNNEngine

from ..common.inout import inform, trim_path, check_output
from engine import EngineExecutionError


class PyNNNestEngine(PyNNEngine):
    
    name = "PyNN_Nest"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               PyNNNestEngine.name, indent=1)
        return PyNNEngine.is_installed(None) and NestEngine.is_installed(None)
        
    @staticmethod
    def install(version):
        if not NestEngine.is_installed(None):
            NestEngine.install(None)
            inform("%s installed Nest..." % PyNNNestEngine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed(None):
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNNestEngine.name, indent=2, verbosity =1)

        PyNNNestEngine.path = PyNNEngine.path + \
            ":" + NestEngine.path
        PyNNNestEngine.environment_vars = {}
        PyNNNestEngine.environment_vars.update(
            PyNNEngine.environment_vars)
        PyNNNestEngine.environment_vars.update(
            NestEngine.environment_vars)
        inform("PATH: " + PyNNNestEngine.path)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'nest'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
















