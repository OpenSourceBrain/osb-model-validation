import os
from omv.common.inout import check_output as co

from utils.wdir import working_dir

def install_pynml():
    
    with working_dir(os.environ['HOME']):
        print(co(['git', 'clone', 'https://github.com/NeuralEnsemble/libNeuroML.git']))
        print(co(['git', 'clone', 'https://github.com/NeuroML/pyNeuroML.git']))
        
    with working_dir(os.path.join(os.environ['HOME'],'libNeuroML')):
        print(co(['git', 'checkout', 'development']))
        print(co(['python', 'setup.py', 'install']))
        
    with working_dir(os.path.join(os.environ['HOME'],'pyNeuroML')):
        print(co(['python', 'setup.py', 'install']))
