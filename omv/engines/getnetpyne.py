import os
import pip
from ..common.inout import inform, check_output
from utils.wdir import working_dir

def install_netpyne():
    install_root = os.environ['HOME']

    with working_dir(install_root):
        print(check_output(['git', 'clone', 'https://github.com/Neurosim-lab/netpyne.git']))

    path = os.path.join(install_root,'netpyne')

    with working_dir(path):
        print(check_output(['git', 'checkout', 'neuroml_export']))
        print(check_output(['pwd']))
        print(check_output(['python', 'setup.py', 'install']))

    m = 'Successfully installed NetPyNE...'
        
