from omv.common.inout import check_output
from omv.engines.utils.wdir import working_dir
import os

def install_netpyne():
    install_root = os.environ['HOME']

    with working_dir(install_root):
        print(check_output(['git', 'clone', 'https://github.com/Neurosim-lab/netpyne.git', 'netpyneInstall']))

    path = os.path.join(install_root,'netpyneInstall')

    with working_dir(path):
        print(check_output(['git', 'checkout', 'neuroml_updates']))
        print(check_output(['pwd']))
        print(check_output(['python', 'setup.py', 'install']))

    m = 'Successfully installed NetPyNE...'
        
