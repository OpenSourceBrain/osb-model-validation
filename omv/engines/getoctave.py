from omv.common.inout import inform, check_output


def install_octave():
    
    inform('Installing Octave', indent=2, verbosity=1)
    
    check_output(['apt-get', 'install', 'octave'])
        

if __name__ == '__main__':
    
    install_octave()










