import os
from subprocess import check_output as co

from omv.common.inout import inform
from omv.engines.utils.wdir import working_dir

install_root = os.environ['HOME']

default_nml2_dir = os.path.join(install_root,'NeuroML2')

def is_nml2_installed():
    history_file = os.path.join(default_nml2_dir,'HISTORY.md')
    if os.path.exists(default_nml2_dir) and os.path.exists(history_file):
        return True
    else:
        return False

def install_nml2():
    
    with working_dir(install_root):
        print(co(['git', 'clone', 'https://github.com/NeuroML/NeuroML2.git']))
    with working_dir(default_nml2_dir):
        print(co(['git', 'checkout', 'development']))
        
    inform('Successfully cloned NeuroML2', indent=2, verbosity=1)
    
