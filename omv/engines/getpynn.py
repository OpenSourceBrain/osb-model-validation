import os
import pip
from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir

def install_pynn():
    try:
        
        pip.main(['install', 'lazyarray'])  # This should ideally be automatically installed with PyNN...
        pip.main(['install', 'neo==0.4.1'])  # This should ideally be automatically installed with PyNN...

        install_root = os.environ['HOME']

        with working_dir(install_root):
            check_output(['git', 'clone', 'https://github.com/NeuralEnsemble/PyNN.git'])

        path = os.path.join(install_root,'PyNN')

        with working_dir(path):
            check_output(['python', 'setup.py', 'install'])
        import pyNN
        m = 'Successfully installed pyNN...'
    except Exception as e:
        m = 'ERROR installing pyNN: ' + str(e)
    finally:
        inform(m)
        
