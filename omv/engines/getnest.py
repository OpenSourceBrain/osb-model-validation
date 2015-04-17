import os
import sys
from ..common.inout import inform, check_output
from distutils.core import run_setup

from utils.wdir import working_dir


def install_nest():
    
    inform('Installing NEST', indent=2, verbosity=1)
    nestpath = os.path.join(os.environ['HOME'],'nest')
    nestpath2 = os.path.join(os.environ['HOME'],'nest/nest')
    os.mkdir(nestpath)
    
    with working_dir(nestpath):
        version='2.6.0'
        check_output(['wget', 'http://www.nest-simulator.org/download/gplreleases/nest-%s.tar.gz'%version])
        #check_output(['cp', '/home/padraig/temp/nest-2.4.2.tar.gz', '.'])
        check_output(['tar', 'xzvf', 'nest-%s.tar.gz'%version])
        check_output(['mv', 'nest-%s'%version, 'nest'], cwd=nestpath)
            
        check_output(["./configure", "--prefix=%s"%(nestpath2)], cwd=nestpath2)
        check_output(['make'], cwd=nestpath2)
        check_output(['make', 'install'], cwd=nestpath2)
        

if __name__ == '__main__':
    
    install_nest()










