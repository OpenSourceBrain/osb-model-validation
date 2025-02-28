import os
import subprocess as sp

from omv.engines.pyneuroml_ import PyNeuroMLEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class MooseEngine(OMVEngine):
    name = "Moose"

    @staticmethod
    def is_installed():
        ret = True
        try:
            import moose

            inform(
                "Moose version %s is correctly installed..." % moose.__version__,
                indent=2,
                verbosity=1,
            )

            ret = "v%s" % moose.__version__

        except Exception as err:
            inform("Couldn't import Moose into Python: ", err, indent=1, verbosity=1)
            ret = False
        return ret

    @staticmethod
    def install(version):
        if not PyNeuroMLEngine.is_installed():
            PyNeuroMLEngine.install(None)
            inform(
                "%s installed PyNeuroML..." % MooseEngine.name, indent=2, verbosity=1
            )

        from omv.engines.getmoose import install_moose

        home = os.environ["HOME"]
        inform("Will fetch and install the latest Moose..", indent=2)
        install_moose(version)
        inform("Done, Moose is correctly installed...", indent=2)

    def run(self):
        try:
            inform(
                "Running file %s with %s" % (trim_path(self.modelpath), self.name),
                indent=1,
            )
            self.stdout = check_output(
                ["python", self.modelpath, "-nogui"],
                cwd=os.path.dirname(self.modelpath),
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: " % self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
