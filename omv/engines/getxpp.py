import os
from omv.common.inout import inform, check_output

from omv.engines.utils.wdir import working_dir
from sysconfig import get_paths
import sys
        
import fileinput


def install_xpp(version='latest'):

    if version is None: 
        version='latest'
    elif not version=='latest':
        raise Exception('Can currently only install the latest XPP version')

    inform("Installing XPP", indent=2, verbosity=1)
    xppinstallpath = os.path.join(os.environ["HOME"])
    xpphomepath = os.path.join(xppinstallpath, 'xppaut')

    inform(
        "Installing XPP to: %s" % (xpphomepath),
        indent=2,
        verbosity=1,
    )
    pypaths = get_paths()
    inform("Python lib info: %s" % (pypaths), indent=2, verbosity=1)


    with working_dir(xppinstallpath):
        print(
            check_output(
                [
                    "git",
                    "clone",
                    "https://github.com/NeuroML/xppaut"
                ]
            )
        )

    with working_dir(xpphomepath):
        print(
            check_output(
                [
                    "ls",
                    "-alth"
                ]
            )
        )

        makefile = os.path.join(xpphomepath, 'Makefile')
                
        print(' - Replacing text in %s'%makefile)
        with open(makefile, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace("/usr/local/", "%s/"%xpphomepath)

        # Write the file out again
        with open(makefile, 'w') as file:
            file.write(filedata)

        print(
            check_output(
                [
                    "make", "-j4"
                ]
            )
        )
        print(
            check_output(
                [
                    "make", "install"
                ]
            )
        )



if __name__ == "__main__":
    install_nest()
