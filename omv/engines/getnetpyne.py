from omv.common.inout import check_output
from omv.engines.utils.wdir import working_dir
from omv.common.inout import pip_install
import os
import sys


def install_netpyne(version=None):
    if version is not None:
        pip_install("netpyne", version)
        import netpyne

    else:
        install_root = os.environ["HOME"]
        install_dir = "netpyneInstall"
        path = os.path.join(install_root, install_dir)

        if not os.path.isdir(path):
            with working_dir(install_root):
                print(
                    check_output(
                        [
                            "git",
                            "clone",
                            "https://github.com/Neurosim-lab/netpyne.git",
                            install_dir,
                        ]
                    )
                )

        with working_dir(path):
            print(check_output(["git", "checkout", "neuroml_updates"]))
            print(check_output(["pwd"]))

        with working_dir(path):
            if sys.version_info.major == 2:
                pip_install(
                    [
                        "kiwisolver==1.0.1",
                        "matplotlib==2.2.4",
                        "pandas==0.23.4",
                        "bokeh==1.4.0",
                        "Pillow==5.4.1",
                        "matplotlib-scalebar==0.5.1",
                        "scipy==1.2.2",
                        "python-dateutil==2.8.0",
                    ]
                )
            pip_install(".")

        m = "Successfully installed NetPyNE..."
