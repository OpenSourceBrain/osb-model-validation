import os
import pip

def install_brian():
    try:
        pip.main(['install', 'brian'])
        import brian
        m = 'Successfully installed Brian...'
    except Exception as e:
        m = 'ERROR installing Brian: ' + str(e)
    finally:
        print m
        
