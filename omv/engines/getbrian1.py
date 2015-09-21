import pip


def check_scipy_dev():
    try:
        import scipy
    except ImportError:
        # Compiling from source is terribly slow, and requires Blas/Lapack...
        #print 'Installing scipy dev...'
        #pip.main(['install', 'cython'])
        #pip.main(['install', 'git+http://github.com/scipy/scipy/'])
        print("\n***************************************************************************************")
        print("\n* ")
        print("\n**  ERROR: Brian requires scipy. Please install it manually.")
        print("\n**  If running OMV on Travis-CI, see https://github.com/OpenSourceBrain/BrianShowcase/blob/master/.travis.yml.")
        print("\n* ")
        print("\n***************************************************************************************")
        raise ImportError


def install_brian():
    try:
        check_scipy_dev()
        pip.main(['install', 'brian'])
        import brian
        m = 'Successfully installed Brian...'
    except Exception as e:
        m = 'ERROR installing Brian: ' + str(e)
    finally:
        print(m)
        
