from omv.common.inout import pip_install

def install_eden(version=None):
    if not version:
        version='0.0.1'
    try:

        pip_install('eden-simulator==%s'%version)
        import eden_simulator
        m = 'Successfully installed EDEN...'
    except Exception as e:
        m = 'ERROR installing EDEN: ' + str(e)
    finally:
        print(m)
