from omv.common.inout import pip_install

from omv.engines.getbrian1 import check_scipy_dev

def install_brian2(version):
    if not version:
        version='2.3'
    try:
        check_scipy_dev()
        # Tested with v2.3     
        
        pip_install('brian2==%s'%version)
        import brian2
        m = 'Successfully installed Brian2...'
    except Exception as e:
        m = 'ERROR installing Brian2: ' + str(e)
    finally:
        print(m)
        