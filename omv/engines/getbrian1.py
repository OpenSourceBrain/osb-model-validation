import os
import pip
from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir


def check_scipy_dev():
    try:
        import scipy
    except ImportError:
        # Compiling from source is terribly slow, and requires Blas/Lapack...
        #print('Installing scipy dev...')
        #pip.main(['install', 'cython'])
        #pip.main(['install', 'git+http://github.com/scipy/scipy/'])
        print("\n***************************************************************************************")
        print("\n* ")
        print("\n**  ERROR: Brian requires scipy. Please install it manually.")
        print("\n**  If running OMV on Travis-CI, see https://github.com/OpenSourceBrain/BrianShowcase/blob/master/.travis.yml.")
        print("\n* ")
        print("\n***************************************************************************************")
        raise ImportError


def install_brian():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        check_output(['git', 'clone', 'https://github.com/brian-team/brian.git'])
        inform('Successfully cloned Brian', indent=2, verbosity=1)
    
    path = os.path.join(install_root,'brian')
    
    with working_dir(path):
        check_output(['git','checkout','master'])
        check_output(['python', 'setup.py', 'install'])
        inform('Successfully installed Brian', indent=2, verbosity=1)
