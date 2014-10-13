import os
from subprocess import check_output as co

from utils.wdir import working_dir

def install_genesis(get_latest=False):
    genpath = os.path.join(os.environ['HOME'], 'genesis')
    os.mkdir(genpath)
    with working_dir(genpath):
        print co(['wget', 'https://raw.githubusercontent.com/borismarin/genesis2.4gamma/genesis23omv/genesis23omv.tgz'])
        print co(['tar', 'xzvf', 'genesis23omv.tgz'])
        print co(['ls', '-la', 'genesis-2.3'])
        os.chdir('genesis-2.3/src')
        print co(['make', 'nxgenesis'])
        print co(['cp', 'startup/travis_simrc',
                  os.path.join(os.environ['HOME'], '.simrc')])










