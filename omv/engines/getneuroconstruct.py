import os
from ..common.inout import inform, check_output as co
from utils.wdir import working_dir

def install_neuroconstruct():
    try:
        
        install_root = os.environ['HOME']

        with working_dir(install_root):
                print co(['git', 'clone', 'https://github.com/NeuralEnsemble/neuroConstruct.git'])
                
        path = os.path.join(install_root,'neuroConstruct')
        
        with working_dir(path):
            print co(['./updatenC.sh'])
            print co(['./nC.sh', '-make'])
            m = 'Successfully installed neuroConstruct...'
        
        
    except Exception as e:
        m = 'ERROR installing neuroConstruct: ' + str(e)
    finally:
        inform(m)
        
