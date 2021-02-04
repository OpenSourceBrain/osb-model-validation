from omv.common.inout import pip_install


def install_pylems():

    try:  
        pip_install('pylems')
        import lems
        m = 'Successfully installed pylems v%s...'%lems.__version__
    except Exception as e:
        m = 'ERROR installing pylems: ' + str(e)
    finally:
        print(m)
        
