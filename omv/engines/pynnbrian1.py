import os
import subprocess as sp

from omv.engines.brian1 import Brian1Engine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNNBrian1Engine(PyNNEngine):
    
    name = "PyNN_Brian1"
    python3_compatible = Brian1Engine.python3_compatible

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
                   PyNNBrian1Engine.name, indent=1)
        return PyNNEngine.is_installed(None) and Brian1Engine.is_installed(None)
        
    @staticmethod
    def install(version):
        if not Brian1Engine.is_installed(None):
            Brian1Engine.install(version)  # interpret version as version of Brian!
            inform("%s installed Brian..." % PyNNBrian1Engine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed(None):
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNBrian1Engine.name, indent=2, verbosity =1)

        PyNNBrian1Engine.path = PyNNEngine.path + \
            ":" + Brian1Engine.path
        PyNNBrian1Engine.environment_vars = {}
        PyNNBrian1Engine.environment_vars.update(
            PyNNEngine.environment_vars)
        PyNNBrian1Engine.environment_vars.update(
            Brian1Engine.environment_vars)
        inform("PATH: " + PyNNBrian1Engine.path)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'brian'],
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
















