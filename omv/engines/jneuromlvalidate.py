import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine, EngineExecutionError
from omv.common.inout import inform, check_output
from omv.engines.engine import PATH_DELIMITER
from omv.engines.utils import resolve_paths


class JNeuroMLValidateEngine(JNeuroMLEngine):
    name = "jNeuroML_validate"

    @staticmethod
    def is_installed():
        return JNeuroMLEngine.is_installed()

    @staticmethod
    def install(version):
        if not JNeuroMLEngine.is_installed():
            JNeuroMLEngine.install(version)

        JNeuroMLValidateEngine.path = JNeuroMLEngine.path
        JNeuroMLValidateEngine.environment_vars = {}
        JNeuroMLValidateEngine.environment_vars.update(JNeuroMLEngine.environment_vars)

    def run(self):
        try:
            path_s = resolve_paths(self.modelpath)

            inform(
                "Path [%s] expanded to: \n        %s" % (self.modelpath, '\n        '.join(path_s)),
                indent=1,
                verbosity=1,
            )
            if len(path_s) == 0:
                raise EngineExecutionError(
                    "Could not determine list of files for validation from string: %s" % self.modelpath
                )

            from omv.engines.jneuroml import JNeuroMLEngine

            jnml = JNeuroMLEngine.get_executable()
            cmds = [jnml, "-validate"]
            for p in path_s:
                cmds.append(p)

            inform(
                "Running with %s, using: %s..." % (JNeuroMLValidateEngine.name, cmds),
                indent=1,
            )
            self.stdout = check_output(
                cmds,
                cwd=os.path.dirname(self.modelpath.split(PATH_DELIMITER)[0]),
                env=JNeuroMLEngine.get_environment(),
            )
            inform(
                "Success with running ",
                JNeuroMLValidateEngine.name,
                indent=1,
                verbosity=1,
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLValidateEngine.name, indent=1, verbosity=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
