import os
import sys

import subprocess as sp

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class XppEngine(OMVEngine):
    name = "XPP"

    @staticmethod
    def get_xpp_environment():
        xpppath = os.path.join(os.environ["HOME"], "xpp/")

        if "XPP_HOME" in os.environ:
            xpppath = os.environ["XPP_HOME"] + "/"

        environment_vars = {
            "XPP_HOME": xpppath,
        }

        return environment_vars

    @staticmethod
    def is_installed():
        ret = True
        environment_vars = XppEngine.get_xpp_environment()
        try:
            FNULL = open(os.devnull, "w")

            r = check_output(
                [environment_vars["XPP_HOME"] + "/xppaut", "-version"], verbosity=2
            )
            ret = "%s" % r.split()[2]
            if not "v" in ret:
                ret = "v%s" % ret

            inform("XPP %s is correctly installed..." % ret, indent=2, verbosity=1)

        except OSError as err:
            if is_verbose():
                inform("Couldn't execute XPP: ", err, indent=1)
            ret = False
        return ret

    @staticmethod
    def install(version):
        from omv.engines.getxpp import install_xpp

        install_xpp(version)
        inform("Done...", indent=2)

    def run(self):
        self.environment_vars = XppEngine.get_xpp_environment()
        self.set_environment()

        try:
            inform(
                "Running file %s with %s" % (trim_path(self.modelpath), self.name),
                indent=1,
            )
            self.stdout = check_output(
                [self.environment_vars["XPP_HOME"] + "/xppaut", self.modelpath, '-silent'],
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
