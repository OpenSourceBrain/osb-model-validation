from omv.common.inout import pip_install, inform

def install_pynml(version=None):

    try:
        pip_install('pyneuroml', version)
        import neuroml
        import pyneuroml
        m = 'Successfully installed pyNeuroML v%s...'%pyneuroml.__version__
    except Exception as e:
        m = 'ERROR installing pyNeuroML: ' + str(e)
    finally:
        inform(m, indent=2)
