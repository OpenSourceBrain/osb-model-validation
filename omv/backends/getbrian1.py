import pip


def install_scipy_dev():
    try:
        import scipy
    except:
        print 'Installing scipy dev...'
        pip.main(['install', 'cython'])
        pip.main(['install', 'git+http://github.com/scipy/scipy/'])
        import scipy


def install_brian():
    try:
        install_scipy_dev()
        pip.main(['install', 'brian'])
        import brian
        m = 'Successfully installed Brian...'
    except Exception as e:
        m = 'ERROR installing Brian: ' + str(e)
    finally:
        print m
        
