import os
import sys
from subprocess import check_output as co
from distutils.core import run_setup
from omv.common.inout import inform

from omv.engines.utils.wdir import working_dir


def install_neuron(get_latest=False):
    nrnpath = os.path.join(os.environ['HOME'],'neuron')
    
    inform('Installing NEURON into %s'%nrnpath, indent=1)
    os.mkdir(nrnpath)
    with working_dir(nrnpath):
        if get_latest:
            print(co(['hg', 'clone', 'http://www.neuron.yale.edu/hg/neuron/nrn']))
            os.chdir('nrn')
            print(co(['./build.sh']))
        else:
            print(co(['wget', 'http://www.neuron.yale.edu/ftp/neuron/versions/v7.3/nrn-7.3.tar.gz']))
            print(co(['tar', 'xzvf', 'nrn-7.3.tar.gz']))
            print(co(['mv', 'nrn-7.3', 'nrn']))
            os.chdir('nrn')
            
        path = os.getcwd()
        pyexec = sys.executable
        co(["./configure --prefix=%s --without-iv --with-nrnpython=%s"%(path,pyexec)], shell=True)
        print(co(['make']))
        print(co(['make', 'install']))

        os.chdir('src/nrnpython')
        run_setup('./setup.py', ['install'])











