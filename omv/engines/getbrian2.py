import pip

from omv.engines.getbrian1 import check_scipy_dev

def install_brian2():
    try:
        check_scipy_dev()
        # Tested with v2.2.2.1
        pip.main(['install', 'brian2==2.2.2.1'])
        import brian2
        m = 'Successfully installed Brian2...'
    except Exception as e:
        m = 'ERROR installing Brian2: ' + str(e)
    finally:
        print(m)
        
