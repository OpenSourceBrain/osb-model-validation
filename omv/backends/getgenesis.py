import os
from subprocess import check_output as co

from utils.wdir import working_dir

def install_genesis(get_latest=False):
    genpath = os.path.join(os.environ['HOME'],'genesis')
    os.mkdir(genpath)
    with working_dir(genpath):
        print co(['wget', 'https://github.com/borismarin/omv-testbed/raw/master/genesis23omv.tgz'])
        print co(['pwd'])
        print co(['tar', 'xzvf', 'genesis23omv.tgz'])
        os.chdir('genesis/src')
        print co(['make'])
        print co(['cp', 'startup/travis_simrc',
                  os.path.join(os.environ['HOME'], '.simrc')])










