import pip
from omv.common.inout import inform

def install_pynml():
    
    try:
        pip.main(['install', 'pyneuroml'])
        import neuroml
        import pyneuroml
        m = 'Successfully installed pyNeuroML...'
    except Exception as e:
        m = 'ERROR installing pyNeuroML: ' + str(e)
    finally:
        inform(m, indent=2)
