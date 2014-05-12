import os
import sys
from subprocess import CalledProcessError, STDOUT, check_output as co
import pip
#from distutils.core import run_setup

from utils.wdir import working_dir

def run_n_log(cmd):
    try:
        co(cmd, stderr=STDOUT)
    except CalledProcessError as cperr:
        print '#ERROR: command [', ' '.join(cperr.cmd), '] failed:'
        print cperr.output
        sys.exit(1)



def install_neuron(get_latest=True):
    nrnpath = os.path.join(os.environ['HOME'],'neuron')
    os.mkdir(nrnpath)
    with working_dir(nrnpath):
        if get_latest:
            print 'Installing cython (required for pyNEURON)...',
            pip.main(['install', 'cython'])
            print 'done!'

            print 'Getting latest NEURON source...',
            run_n_log(['hg', 'clone', 'http://www.neuron.yale.edu/hg/neuron/nrn'])
            os.chdir('nrn')
            run_n_log(['./build.sh'])
            print 'done!'
        else:
            print 'Getting NEURON 7.3...', 
            run_n_log(['wget', 'http://www.neuron.yale.edu/ftp/neuron/versions/v7.3/nrn-7.3.tar.gz'])
            run_n_log(['tar', 'xzvf', 'nrn-7.3.tar.gz'])
            run_n_log(['mv', 'nrn-7.3', 'nrn'])
            os.chdir('nrn')
            print 'done!'
            
        print 'CWD:', os.getcwd()
        path = os.getcwd()
        pyexec = sys.executable
        print 'Building NEURON...',
        run_n_log(['./configure', '--prefix=%s'%path, '--without-iv', '--with-nrnpython=%s'%pyexec, '--enable-pysetup'])
        run_n_log(['make'])
        run_n_log(['make', 'install'])
        print 'done!'

         #print 'Installing pyNEURON...', 
        #os.chdir('src/nrnpython')
        #run_setup('./setup.py', ['install'])
        #print 'done!'
















