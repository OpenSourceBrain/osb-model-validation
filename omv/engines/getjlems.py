import os
from subprocess import check_output as co

from omv.common.inout import inform
from omv.engines.utils.wdir import working_dir

def install_jlems():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        print(co(['git', 'clone', 'https://github.com/LEMS/jLEMS.git']))
        inform('Successfully cloned jLEMS', indent=2, verbosity=1)
        
    path = os.path.join(install_root,'jLEMS')
    
    with working_dir(path):
        print(co(['git', 'checkout', 'development']))
        print(co(['mvn', 'install']))
        inform('Successfully installed jLEMS', indent=2, verbosity=1)
