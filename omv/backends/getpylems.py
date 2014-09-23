import os
from subprocess import check_output as co

from utils.wdir import working_dir

def install_pylems():
    path = os.path.join(os.environ['HOME'],'pylems')
    print co(['git', 'clone', 'https://github.com/LEMS/pylems.git'])
    with working_dir(path):
        print co(['python', 'setup.py', 'install'])
