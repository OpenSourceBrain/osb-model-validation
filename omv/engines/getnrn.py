import os
import sys
from subprocess import check_output as co
from distutils.core import run_setup
from omv.common.inout import inform

from omv.engines.utils.wdir import working_dir


def install_neuron(version):
    if not version:
        version='7.6'
        
    nrnpath = os.path.join(os.environ['HOME'],'neuron')
    
    inform('Installing NEURON %s into %s'%(version, nrnpath), indent=1)
    os.mkdir(nrnpath)
    with working_dir(nrnpath):
        print(co(['wget', 'https://www.neuron.yale.edu/ftp/neuron/versions/v%s/nrn-%s.tar.gz'%(version, version)]))
        print(co(['tar', 'xzvf', 'nrn-%s.tar.gz'%version]))
        print(co(['mv', 'nrn-%s'%version, 'nrn']))
        os.chdir('nrn')
            
        path = os.getcwd()
        pyexec = sys.executable
        co(["./configure --prefix=%s --without-iv --with-nrnpython=%s"%(path,pyexec)], shell=True)
        print(co(['make','-j4']))
        print(co(['make', 'install']))

        os.chdir('src/nrnpython')
        run_setup('./setup.py', ['install'])











