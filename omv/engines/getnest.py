import os
from omv.common.inout import inform, check_output

from omv.engines.utils.wdir import working_dir


def install_nest(version):
    
    if not version:
        version='2.18.0'
        
    inform('Installing NEST', indent=2, verbosity=1)
    nestpath = os.path.join(os.environ['HOME'],'nest')
    nestpath2 = os.path.join(os.environ['HOME'],'nest/nest')
    nestinstallpath = os.path.join(os.environ['HOME'],'nest/nest')
    if 'NEST_INSTALL_DIR' in os.environ:
            nestinstallpath = os.environ['NEST_INSTALL_DIR']+'/'
            
    inform('Installing NEST (src: %s), (tgt: %s)'%(nestpath, nestinstallpath), indent=2, verbosity=1)
    os.mkdir(nestpath)
    
    with working_dir(nestpath):
        #version='2.10.0'
        check_output(['wget', 'https://github.com/nest/nest-simulator/archive/v%s.tar.gz'%(version)])
        
        check_output(['tar', 'xzvf', 'v%s.tar.gz'%version])
        check_output(['mv', 'nest-simulator-%s'%version, 'nest'], cwd=nestpath)
            
    with working_dir(nestpath2):
        check_output(["cmake", "-DCMAKE_INSTALL_PREFIX:PATH=%s"%(nestinstallpath)])
        check_output(['make','-j4'])
        check_output(['make', 'install'])
        
        

if __name__ == '__main__':
    
    install_nest()










