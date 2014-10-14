import os
from subprocess import check_output as co

from ..common.inout import inform
from utils.wdir import working_dir

def install_brian():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        print co(['pip', 'install', 'brian'])
        inform('Successfully installed Brian', indent=2, verbosity=1)
        
