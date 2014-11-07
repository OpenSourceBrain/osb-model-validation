import os
from subprocess import check_output as co

from utils.wdir import working_dir


def install_genesis(get_latest=False):
    genpath = os.path.join(os.environ['HOME'], 'genesis')
    os.mkdir(genpath)
    with working_dir(genpath):
        print co(['wget',
                  'https://github.com/borismarin/genesis2.4gamma/archive/master.zip'])
        print co(['tar', 'xzvf', 'master.zip'])
        print co(['ls', '-la', 'genesis2.4gamma-master'])
        os.chdir('genesis2.4gamma-master/src')
        print co(['make', 'nxgenesis'])
        print co(['cp', 'startup/travis_simrc',
                  os.path.join(os.environ['HOME'], '.simrc')])










