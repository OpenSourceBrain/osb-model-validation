from omv.common.inout import check_output, inform

def install_pynml():
    
    try:
        print(check_output(['pip', 'install', 'pyneuroml']))
        import neuroml
        import pyneuroml
        m = 'Successfully installed pyNeuroML...'
    except Exception as e:
        m = 'ERROR installing pyNeuroML: ' + str(e)
    finally:
        inform(m, indent=2)
