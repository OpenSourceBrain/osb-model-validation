import pip


def install_scipy_dev():
    try:
        import scipy
    except ImportError:
        # Compiling from source is terribly slow, and requires Blas/Lapack...
        #print 'Installing scipy dev...'
        #pip.main(['install', 'cython'])
        #pip.main(['install', 'git+http://github.com/scipy/scipy/'])
        print("ERROR: Brian2 requires scipy. Please install it manually.")
        raise ImportError


def install_brian2():
    try:
        install_scipy_dev()
        pip.main(['install', 'brian2'])
        import brian2
        m = 'Successfully installed Brian2...'
    except Exception as e:
        m = 'ERROR installing Brian2: ' + str(e)
    finally:
        print(m)
        
