import os
import pip
from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir

def install_moose():
    install_root = os.environ['HOME']

    with working_dir(install_root):
        print(check_output(['git', 'clone', 'https://github.com/OpenSourceBrain/moose-core.git']))

    with working_dir(os.path.join(install_root,'moose-core')):
        print(check_output(['git', 'checkout', 'nml2_updates_3']))


    with working_dir(os.path.join(install_root,'moose-core')):
        print(check_output(['pwd']))
        print(check_output(['which', 'python']))
        print(check_output(['python', 'setup.py', 'install']))

    m = 'Successfully installed Moose...'
