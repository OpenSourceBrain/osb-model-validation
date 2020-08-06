import os
import subprocess as sp

from omv.engines.nestsli import NestEngine
from omv.engines.pynest import PyNestEngine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNNNestEngine(PyNNEngine):
    
    name = "PyNN_Nest"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
                   PyNNNestEngine.name, indent=1)
        return PyNNEngine.is_installed(None) and PyNestEngine.is_installed(None)
        
    @staticmethod
    def install(version):
        if not PyNestEngine.is_installed(None):
            PyNestEngine.install(version)  # interpret version as version of NEST!
            inform("%s installed PyNest..." % PyNNNestEngine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed(None):
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNNestEngine.name, indent=2, verbosity =1)



    def run(self):
        try:

            self.environment_vars = NestEngine.get_nest_environment()
            self.set_environment()

            inform("Env vars: %s" % self.environment_vars, indent=2)
        
            inform("Running a file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
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
















