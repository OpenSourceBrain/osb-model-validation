import os
from subprocess import check_output as co

from utils.wdir import working_dir

def install_pynml():
    pynmlpath = os.path.join(os.environ['HOME'],'pynml')
    os.mkdir(pynmlpath)
    with working_dir(pynmlpath):
        print(co(['git', 'clone', 'https://github.com/NeuralEnsemble/libNeuroML.git']))
        print(co(['cd', 'libNeuroML']))
        print(co(['git', 'checkout', 'development']))
        print(co(['python', 'setup.py', 'install']))
        print(co(['cd', '..']))
        print(co(['git', 'clone', 'https://github.com/NeuroML/pyNeuroML.git']))
        print(co(['python', 'setup.py', 'install']))
