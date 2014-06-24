import os
from subprocess import check_output as co

from utils.wdir import working_dir

def install_jlems():
    path = os.path.join(os.environ['HOME'],'jLEMS')
    print co(['git', 'clone', 'https://github.com/LEMS/jLEMS.git'])
    with working_dir(path):
        print co(['mvn', 'install'])
