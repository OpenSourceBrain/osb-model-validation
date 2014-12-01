import pip
from ..common.inout import inform

def install_pynn():
    try:
        pip.main(['install', 'pyNN'])
        import pyNN
        m = 'Successfully installed pyNN...'
    except Exception as e:
        m = 'ERROR installing pyNN: ' + str(e)
    finally:
        inform(m)
        
