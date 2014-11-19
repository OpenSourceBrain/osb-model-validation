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
        execute(['conda', 'create', '-p', '$HOME/py', '--yes', 'pip', 'numpy', 'scipy', 'python'])
        execute(['sudo', 'pip', 'install', 'brian'])
        
        inform('Finished installing, testing...', indent=2, verbosity=1)
        import brian
        inform('Successfully installed Brian version %s'%brian.__version__, indent=2, verbosity=1)
        
