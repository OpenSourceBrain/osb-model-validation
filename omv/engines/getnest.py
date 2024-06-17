import os
from omv.common.inout import inform, check_output

from omv.engines.utils.wdir import working_dir
from sysconfig import get_paths
import sys


def install_nest(version):
    if not version:
        version = "3.5"

    inform("Installing NEST", indent=2, verbosity=1)
    nestpath = os.path.join(os.environ["HOME"], "nest")
    nestpath2 = os.path.join(os.environ["HOME"], "nest/nest")
    nestinstallpath = os.path.join(os.environ["HOME"], "nest/nest")
    if "NEST_INSTALL_DIR" in os.environ:
        nestinstallpath = os.environ["NEST_INSTALL_DIR"] + "/"

    inform(
        "Installing NEST (src: %s), (tgt: %s)" % (nestpath, nestinstallpath),
        indent=2,
        verbosity=1,
    )
    pypaths = get_paths()
    inform("Python lib info: %s" % (pypaths), indent=2, verbosity=1)

    try:
        os.mkdir(nestpath)
    except:
        pass

    with working_dir(nestpath):
        # version='2.10.0'
        check_output(
            [
                "wget",
                "-nv",
                "https://github.com/nest/nest-simulator/archive/v%s.tar.gz" % (version),
            ]
        )
        check_output(["tar", "xzvf", "v%s.tar.gz" % version])
        check_output(["mv", "nest-simulator-%s" % version, "nest"], cwd=nestpath)

    with working_dir(nestpath2):
        check_output(
            [
                "cmake",
                "-DCMAKE_INSTALL_PREFIX:PATH=%s" % nestinstallpath,
                "-DPYTHON_EXECUTABLE:FILEPATH=%s" % (sys.executable),
                "-DPYTHON_INCLUDE_DIR=%s" % pypaths["include"],
                ".",
            ]
        )
        # "-DPYTHON_LIBRARY=%s/libpython3.8m.so" % pypaths['stdlib'],
        # -DPYTHON_INCLUDE_DIR2=/usr/include/x86_64-linux-gnu/python3.4m"%(nestinstallpath, pypaths['scripts'], pypaths['stdlib'], pypaths['include'], pypaths[''])])
        check_output(["make", "-j7"])
        check_output(["make", "install"])


if __name__ == "__main__":
    install_nest()
