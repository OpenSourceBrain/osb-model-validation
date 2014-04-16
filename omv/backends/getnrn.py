import os
import sys
from subprocess import check_output as co
from distutils.core import run_setup

from utils.wdir import working_dir


def install_neuron():
    nrnpath = os.path.join(os.environ['HOME'],'neuron')
    os.mkdir(nrnpath)
    with working_dir(nrnpath):
        print co(['hg', 'clone', 'http://www.neuron.yale.edu/hg/neuron/nrn'])
        os.chdir('nrn')
        print co(['./build.sh'])
        path = os.getcwd()
        pyexec = sys.executable
        co(["./configure --prefix=%s --without-iv --with-nrnpython=%s"%(path,pyexec)], shell=True)
        print co(['make'])
        print co(['make', 'install'])

        os.chdir('src/nrnpython')
        run_setup('./setup.py', ['install'])

