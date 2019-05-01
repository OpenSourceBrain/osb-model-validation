import os
from omv.common.inout import inform, check_output
from omv.engines.utils.wdir import working_dir

def install_pynn():
    try:
        
        print(check_output(['pip', 'install', 'lazyarray']))  # This should ideally be automatically installed with PyNN...
        print(check_output(['pip', 'install', 'neo==0.5.1']))  # This should ideally be automatically installed with PyNN...

        install_root = os.environ['HOME']

        pyNN_src = 'PyNN_src'
        with working_dir(install_root):
            check_output(['git', 'clone', 'https://github.com/NeuralEnsemble/PyNN.git', pyNN_src])

        path = os.path.join(install_root, pyNN_src)

        with working_dir(path):
            print(check_output(['git','checkout','neuroml']))  # neuroml branch has the latest NML2 import/export code!
            #check_output(['git','checkout','master'])
            print(check_output(['python', 'setup.py', 'install']))
            print(check_output(['pwd']))
            print("Finished attempting to install PyNN")
        #import pyNN
        m = 'Successfully installed pyNN...'
    except Exception as e:
        m = 'ERROR during install_pynn: %s'%e
    finally:
        inform(m)
        
