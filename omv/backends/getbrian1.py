import os
from subprocess import check_output as co

from ..common.inout import inform
from utils.wdir import working_dir

def execute(cmds):
    print("Executing: %s"%cmds)
    print(co(cmds))
    

def install_brian():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        execute(['sudo', 'pip', 'install', 'conda'])
        execute(['sudo', 'conda', 'init'])
        execute(['conda', 'create', '-p', '$HOME/py', '--yes', "'numpy scipy'"])
        execute(['sudo', 'pip', 'install', 'brian'])
        import brian
        inform('Successfully installed Brian version %s'%brian.__version__, indent=2, verbosity=1)
        
