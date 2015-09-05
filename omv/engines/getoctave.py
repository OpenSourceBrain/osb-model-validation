

from ..common.inout import inform, check_output

from utils.wdir import working_dir


def install_octave():
    
    inform('Installing Octave', indent=2, verbosity=1)
    
    check_output(['sudo', 'apt-get', 'install', 'octave'])
        

if __name__ == '__main__':
    
    install_nest()










