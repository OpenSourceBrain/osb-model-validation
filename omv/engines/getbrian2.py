import pip

from getbrian1 import check_scipy_dev

def install_brian2():
    try:
        check_scipy_dev()
        pip.main(['install', '--pre', 'brian2'])
        import brian2
        m = 'Successfully installed Brian2...'
    except Exception as e:
        m = 'ERROR installing Brian2: ' + str(e)
    finally:
        print(m)
        
