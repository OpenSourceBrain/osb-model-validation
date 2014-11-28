import pip


def install_pynn():
    try:
        pip.main(['install', 'pyNN'])
        import brian
        m = 'Successfully installed pyNN...'
    except Exception as e:
        m = 'ERROR installing pyNN: ' + str(e)
    finally:
        print(m)
        
