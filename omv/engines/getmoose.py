import os
import pip
from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir

def install_moose():
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        print(check_output(['git', 'clone', 'https://github.com/pgleeson/moose-core.git']))

    with working_dir(os.path.join(install_root,'moose-core')):
        print(check_output(['mkdir', 'build_']))
        
    with working_dir(os.path.join(install_root,'moose-core/build_')):
        print(check_output(['cmake', '..']))
        print(check_output(['make','-j4']))
        print(check_output(['make', 'install']))
        
    with working_dir(os.path.join(install_root,'moose-core/build_/python')):
        print(check_output(['pwd']))
        print(check_output(['python', 'setup.py', 'install']))

    m = 'Successfully installed Moose...' 
        
