from omv.common.inout import check_output

from omv.engines.getbrian1 import check_scipy_dev

def install_brian2(version='2.2.2.1'):
    try:
        check_scipy_dev()
        # Tested with v2.2.2.1     
        print(check_output(['pip', 'install', 'brian2==%s'%version]))
        import brian2
        m = 'Successfully installed Brian2...'
    except Exception as e:
        m = 'ERROR installing Brian2: ' + str(e)
    finally:
        print(m)
        