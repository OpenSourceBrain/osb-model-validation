from omv.common.inout import check_output
from omv.engines.utils.wdir import working_dir
from omv.common.inout import pip_install
import os


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
            pip_install(".")

        m = "Successfully installed NetPyNE..."
