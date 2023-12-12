from omv.common.inout import pip_install, inform


def install_libsbml(version=None):
    try:
        pip_install("python-libsbml", version)
        import libsbml

        m = "Successfully installed libsbml v%s..." % libsbml.__version__
    except Exception as e:
        m = "ERROR installing libsbml: " + str(e)
    finally:
        inform(m, indent=2)
