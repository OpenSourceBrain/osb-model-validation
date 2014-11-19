import os
from subprocess import check_output as co

from ..common.inout import inform
from utils.wdir import working_dir

def execute(cmds):
    inform("Executing: %s"%cmds, indent=1, verbosity=1)
    inform(co(cmds), indent=1)
    

def install_brian():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        execute(['sudo', 'pip', 'install', 'conda'])
        execute(['sudo', 'conda', 'init'])
        execute(['conda', 'create', '-p', 'conda_libs', '--yes', 'pip', 'numpy', 'scipy', 'python=2.7.8'])
        execute(['easy_install', 'brian'])
        
        #inform('Finished installing, testing...', indent=2, verbosity=1)
        #import brian
        inform('Successfully installed Brian...', indent=2, verbosity=1)
        
