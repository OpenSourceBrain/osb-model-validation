from omv.common.inout import pip_install

def install_arbor(version=None):
    if not version:
        version='0.5.2'
    try:

        pip_install('arbor==%s'%version)
        import arbor
        m = 'Successfully installed Arbor...'
    except Exception as e:
        m = 'ERROR installing Arbor: ' + str(e)
    finally:
        print(m)
