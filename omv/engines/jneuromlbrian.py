import os
import subprocess as sp

from jneuroml import JNeuroMLBackend
from brian1 import Brian1Backend
from ..common.inout import inform, trim_path, check_output
from backend import BackendExecutionError


class JNeuroMLBrianBackend(JNeuroMLBackend):

    name = "jNeuroML_Brian"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               JNeuroMLBrianBackend.name, indent=1)
        return JNeuroMLBackend.is_installed(None) and Brian1Backend.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLBackend.is_installed(None):
            JNeuroMLBackend.install(None)
        if not Brian1Backend.is_installed(None):
            Brian1Backend.install(None)

        JNeuroMLBrianBackend.path = JNeuroMLBackend.path + \
            ":" + BrianBackend.path
        JNeuroMLBrianBackend.environment_vars = {}
        JNeuroMLBrianBackend.environment_vars.update(
            JNeuroMLBackend.environment_vars)
        JNeuroMLBrianBackend.environment_vars.update(
            BrianBackend.environment_vars)
        inform("PATH: " + JNeuroMLBrianBackend.path)
        inform("Env vars: %s" % JNeuroMLBrianBackend.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLBrianBackend.name), indent=1)
            self.stdout = check_output(['jnml', self.modelpath, '-brian'], cwd=os.path.dirname(self.modelpath))
            self.stdout += check_output(['python', self.modelpath.replace('.xml', '_brian.py'), '-nogui'], cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLBrianBackend.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLBrianBackend.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
