import os
import subprocess as sp

from omv.engines.pyneuroml_ import PyNeuroMLEngine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNNNeuroMLEngine(PyNNEngine):
    
    name = "PyNN_NeuroML"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
                   PyNNNeuroMLEngine.name, indent=1)
        return PyNNEngine.is_installed(None) and PyNeuroMLEngine.is_installed(None)
        
    @staticmethod
    def install(version):
        if not PyNeuroMLEngine.is_installed(None):
            PyNeuroMLEngine.install(None)
            inform("%s installed PyNeuroML..." % PyNNNeuroMLEngine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed(None):
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNNeuroMLEngine.name, indent=2, verbosity =1)



    def run(self):
        try:

            inform("Env vars: %s" % self.environment_vars, indent=2)
        
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'neuroml'],
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
















