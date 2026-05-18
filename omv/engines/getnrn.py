import os
import sys
import re
from subprocess import check_output as co
from omv.common.inout import inform
from omv.common.inout import pip_install

from omv.engines.utils.wdir import working_dir

DEFAULT_NEURON_VERSION = "8.2.7"


def _supports_pip_install(version):
    return bool(re.match(r"^7\.8($|\.)|^8\.", version))


def install_neuron(version):
    if not version:
        version = DEFAULT_NEURON_VERSION

    if _supports_pip_install(version):
        pip_install("neuron==%s" % version)
        import neuron

        inform("Successfully installed NEURON v%s using pip.." % version, indent=2)
    else:
        nrnpath = os.path.join(os.environ["HOME"], "neuron")

        inform("Installing NEURON %s into %s" % (version, nrnpath), indent=1)
        os.mkdir(nrnpath)
        with working_dir(nrnpath):
            nrn_url = (
                "https://www.neuron.yale.edu/ftp/neuron/versions/v%s/nrn-%s.tar.gz"
                % (version, version)
            )
            dl_file = "nrn-%s.tar.gz" % version

            print(co(["wget", "-nv", nrn_url]))
            print(co(["tar", "xzvf", dl_file]))
            print(co(["mv", "nrn-%s" % version, "nrn"]))
            os.chdir("nrn")

            path = os.getcwd()
            pyexec = sys.executable
            # Needs to be updated if Neuron >=7.8...
            co(
                [
                    "./configure --prefix=%s --without-iv --with-nrnpython=%s"
                    % (path, pyexec)
                ],
                shell=True,
            )
            print(co(["make", "-j3"]))
            print(co(["make", "install"]))

            os.chdir("src/nrnpython")
            print(co(["pip", "install", "."]))
