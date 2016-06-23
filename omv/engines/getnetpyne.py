import os
import pip
from ..common.inout import inform, check_output
from utils.wdir import working_dir

def install_netpyne():
    try:
    
        install_root = os.environ['HOME']

        with working_dir(install_root):
            check_output(['git', 'clone', 'https://github.com/Neurosim-lab/netpyne.git'])
            check_output(['git', 'checkout', 'neuroml_export'])

        path = os.path.join(install_root,'netpyne')

        with working_dir(path):
            check_output(['python', 'setup.py', 'install'])
        import netpyne
        m = 'Successfully installed NetPyNE...'
    except Exception as e:
        m = 'ERROR installing NetPyNE: ' + str(e)
    finally:
        inform(m)
        
