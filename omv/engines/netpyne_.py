import os
import subprocess as sp

from omv.engines.pyneuron import PyNRNEngine
from omv.engines.pyneuroml_ import PyNeuroMLEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class NetPyNEEngine(OMVEngine):
    name = "NetPyNE"

    @staticmethod
    def is_installed(silent=True):
        if is_verbose():
            inform(
                "Checking whether the engine %s has been installed correctly..."
                % NetPyNEEngine.name,
                indent=1,
            )

        ret = True
        try:
            ret_str = sp.check_output(
                ['python -c "import netpyne; print(netpyne.__version__)"'],
                shell=True,
                stderr=sp.STDOUT,
            )

            ret = len(ret_str) > 0

            if isinstance(ret_str, bytes):
                ret_str = ret_str.decode("utf-8")

            ret_str = ret_str.strip().split("\n")[
                -1
            ]  # in case multiple lines (with warning) returned

            if ret and is_verbose():
                inform("%s is correctly installed..." % (NetPyNEEngine.name), indent=2)

            if ret:
                ret = "v%s" % str(ret_str.strip())

        except Exception as err:
            if not silent:
                inform("Couldn't import netpyne into Python: ", err, indent=1)
            ret = False

        if not PyNRNEngine.is_installed() or not PyNeuroMLEngine.is_installed():
            ret = False

        if not silent:
            inform("NetPyNE is_installed: %s" % ret, "", indent=1)
        return ret

    @staticmethod
    def install(version):
        if not PyNRNEngine.is_installed():
            PyNRNEngine.install(None)
            inform(
                "%s installed PyNEURON..." % NetPyNEEngine.name, indent=2, verbosity=1
            )

        if not PyNeuroMLEngine.is_installed():
            PyNeuroMLEngine.install(None)
            inform(
                "%s installed PyNeuroML..." % NetPyNEEngine.name, indent=2, verbosity=1
            )

        from omv.engines.getnetpyne import install_netpyne

        home = os.environ["HOME"]
        inform("Will fetch and install the latest NetPyNE..", indent=2)
        install_netpyne(version)
        inform("Done, NetPyNE is correctly installed...", indent=2)

        NetPyNEEngine.path = PyNRNEngine.path
        NetPyNEEngine.environment_vars = {}
        NetPyNEEngine.environment_vars.update(PyNRNEngine.environment_vars)

        inform("PATH: " + NetPyNEEngine.path, indent=2, verbosity=1)
        inform("Env vars: %s" % NetPyNEEngine.environment_vars, indent=2, verbosity=1)

        environment_vars, path = PyNRNEngine.get_nrn_environment()
        inform(
            "Using NEURON with env %s at %s..." % (environment_vars, path),
            indent=2,
            verbosity=1,
        )

        # print(check_output([environment_vars['NEURON_HOME']+'/bin/nrnivmodl'], cwd=pynn_mod_dir)

    def run(self):
        try:
            self.stdout = PyNRNEngine.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform("Error compiling modfiles:", self.stderr, indent=2)

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
