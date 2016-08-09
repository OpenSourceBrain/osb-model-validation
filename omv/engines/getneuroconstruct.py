import os
import pip
from ..common.inout import inform, check_output
from utils.wdir import working_dir

def install_neuroconstruct():
    try:
        
        install_root = os.environ['HOME']
        
        # Install nC by:
        # 1) cloning local copy of https://github.com/NeuralEnsemble/neuroConstruct.git
        # 2) running: ./nC.sh -make 
        
        
    except Exception as e:
        m = 'ERROR installing neuroConstruct: ' + str(e)
    finally:
        inform(m)
        
