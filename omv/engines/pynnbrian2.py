import os
import subprocess as sp

from omv.engines.brian2_ import Brian2Engine
from omv.engines.pynn import PyNNEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class PyNNBrian2Engine(PyNNEngine):
    
    name = "PyNN_Brian2"
    python3_compatible = Brian2Engine.python3_compatible

    @staticmethod
    def is_installed():
        if is_verbose():
            inform("Checking whether %s is installed..." %
                   PyNNBrian2Engine.name, indent=1)
        return PyNNEngine.is_installed() and Brian2Engine.is_installed()
        
    @staticmethod
    def install(version):
        if not Brian2Engine.is_installed():
            Brian2Engine.install(version)  # interpret version as version of Brian!
            inform("%s installed Brian..." % PyNNBrian2Engine.name, indent=2, verbosity =1)
        if not PyNNEngine.is_installed():
            PyNNEngine.install(None)
            inform("%s installed PyNN..." % PyNNBrian2Engine.name, indent=2, verbosity =1)

        PyNNBrian2Engine.path = PyNNEngine.path + \
            ":" + Brian2Engine.path
        PyNNBrian2Engine.environment_vars = {}
        PyNNBrian2Engine.environment_vars.update(
            PyNNEngine.environment_vars)
        PyNNBrian2Engine.environment_vars.update(
            Brian2Engine.environment_vars)
        inform("PATH: " + PyNNBrian2Engine.path)


    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, 'brian2'],
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
















