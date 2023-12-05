import os
from omv.common.inout import inform, check_output

from omv.engines.utils.wdir import working_dir
from sysconfig import get_paths
import sys


def install_xpp(version='latest'):

    if version is None: 
        version='latest'
    elif not version=='latest':
        raise Exception('Can currently only install the latest XPP tarball')

    inform("Installing XPP", indent=2, verbosity=1)
    xppinstallpath = os.path.join(os.environ["HOME"], "xpp")

    inform(
        "Installing XPP to: %s" % (xppinstallpath),
        indent=2,
        verbosity=1,
    )
    pypaths = get_paths()
    inform("Python lib info: %s" % (pypaths), indent=2, verbosity=1)

    try:
        os.mkdir(xppinstallpath)
    except:
        pass

    with working_dir(xppinstallpath):
        
        check_output(
            [
                "wget",
                "-nv",
                "https://sites.pitt.edu/~phase/bard/bardware/binary/%s/xpplinux.tgz" % (version),
            ]
        )
        check_output(["tar", "xzvf", "xpplinux.tgz"])
        check_output(["mv", "xppaut8.0ubuntu", "xppaut"])



if __name__ == "__main__":
    install_nest()
