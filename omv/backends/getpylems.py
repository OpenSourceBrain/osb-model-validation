import os
from subprocess import check_output as co

from ..common.inout import inform
from utils.wdir import working_dir

def install_pylems():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        print co(['git', 'clone', 'https://github.com/LEMS/pylems.git'])
        inform('Successfully cloned PyLEMS', indent=2, verbosity=1)
    
    path = os.path.join(install_root,'pylems')
    
    with working_dir(path):
        print co(['python', 'setup.py', 'install'])
        inform('Successfully installed PyLEMS', indent=2, verbosity=1)
        
# TODO: Move to getnml2
def install_nml2():
    print co(['git', 'clone', 'https://github.com/NeuroML/NeuroML2.git'])
