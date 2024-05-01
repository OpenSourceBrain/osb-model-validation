import os
from omv.common.inout import inform, check_output
from omv.common.inout import pip_install

from omv.engines.utils.wdir import working_dir


def install_pynn(version=None):
    if not version:
        version = "0.11.0"

    try:
        # pip_install('lazyarray')  # This should ideally be automatically installed with PyNN...
        # pip_install('neo>=0.11.0')  # This should ideally be automatically installed with PyNN...

        install_root = os.environ["HOME"]

        pyNN_src = "PyNN_src"
        with working_dir(install_root):
            check_output(
                ["git", "clone", "https://github.com/NeuralEnsemble/PyNN.git", pyNN_src]
            )

        path = os.path.join(install_root, pyNN_src)

        with working_dir(path):
            print(
                check_output(["git", "checkout", version])
            )  # neuroml branch has the latest NML2 import/export code!
            # check_output(['git','checkout','master'])
            # print(check_output(['python', 'setup.py', 'install']))
            pip_install(".")
            print(check_output(["pwd"]))
            print("Finished attempting to install PyNN")
        # import pyNN
        m = "Successfully installed pyNN..."
    except Exception as e:
        m = "ERROR during install_pynn: %s" % e
    finally:
        inform(m)
