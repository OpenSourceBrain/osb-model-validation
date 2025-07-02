import os
import shutil
import subprocess as sp
from pathlib import Path

from omv.common.inout import check_output, inform, is_verbose, trim_path
from omv.engines.engine import EngineExecutionError, OMVEngine


class JNeuroMLEngine(OMVEngine):
    name = "jNeuroML"
    e_name = "jnml"

    @staticmethod
    def get_environment():
        if "JNML_HOME" in os.environ:
            jnmlhome = os.environ["JNML_HOME"]
        elif shutil.which(JNeuroMLEngine.e_name) is not None:
            jnmlhome = Path(shutil.which(JNeuroMLEngine.e_name)).parent
        else:
            jnmlhome = ""

        environment_vars = {"JNML_HOME": jnmlhome}

        return environment_vars

    @staticmethod
    def get_executable():
        environment_vars = JNeuroMLEngine.get_environment()
        jnml = os.path.join(environment_vars["JNML_HOME"], JNeuroMLEngine.e_name)
        return jnml

    @staticmethod
    def is_installed():
        ret = True
        try:
            if is_verbose():
                inform(
                    "Checking whether %s is installed..." % JNeuroMLEngine.name,
                    indent=1,
                )
            jnml = JNeuroMLEngine.get_executable()
            r = check_output(
                [jnml, "-v"], verbosity=2, env=JNeuroMLEngine.get_environment()
            )
            ret = "%s" % r.split()[1]

            if is_verbose():
                inform("%s %s is installed..." % (JNeuroMLEngine.name, ret), indent=2)
        except OSError as err:
            if is_verbose():
                inform("Couldn't execute/import jNeuroML: ", err, indent=1)
            ret = False
        return ret

    @staticmethod
    def install(version):
        from omv.engines.getpyneuroml import install_pynml

        inform("Will install PyNeuroML for jnml", indent=2)
        install_pynml(version)

        if not JNeuroMLEngine.is_installed():
            inform("Failure to install, exiting", indent=1)
            exit(1)

    def run(self):
        try:
            inform(
                "Running file %s with %s" % (trim_path(self.modelpath), self.name),
                indent=1,
            )

            jnml = JNeuroMLEngine.get_executable()
            self.stdout = sp.check_output(
                [jnml, self.modelpath, "-nogui"],
                cwd=os.path.dirname(self.modelpath),
                env=JNeuroMLEngine.get_environment(),
            )
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
