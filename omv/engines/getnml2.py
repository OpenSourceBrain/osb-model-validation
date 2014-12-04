import os
from subprocess import check_output as co

from ..common.inout import inform
from utils.wdir import working_dir

install_root = os.environ['HOME']

default_nml2_dir = os.path.join(install_root,'NeuroML2')


def install_nml2():
    
    with working_dir(install_root):
        print co(['git', 'clone', 'https://github.com/NeuroML/NeuroML2.git'])
        inform('Successfully cloned NeuroML2', indent=2, verbosity=1)
    
