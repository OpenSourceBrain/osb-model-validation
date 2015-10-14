import pip
from ..common.inout import inform

def install_pynn():
    try:
        pip.main(['install', 'lazyarray'])  # This should ideally be automatically installed with PyNN...
        pip.main(['install', 'neo'])  # This should ideally be automatically installed with PyNN...
        pip.main(['install', 'pyNN'])
        import pyNN
        m = 'Successfully installed pyNN...'
    except Exception as e:
        m = 'ERROR installing pyNN: ' + str(e)
    finally:
        inform(m)
        
