import os

from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir

def install_pylems():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        check_output(['git', 'clone', 'https://github.com/LEMS/pylems.git'])
        inform('Successfully cloned PyLEMS', indent=2, verbosity=1)
    
    path = os.path.join(install_root,'pylems')
    
    with working_dir(path):
        check_output(['python', 'setup.py', 'install'])
        inform('Successfully installed PyLEMS', indent=2, verbosity=1)
        
