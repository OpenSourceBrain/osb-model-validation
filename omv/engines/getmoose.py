from omv.common.inout import pip_install


def install_moose(version):
    if not version:
        version = "4.0.0.dev20240411"
        version = "4.1.4" # temp test this, it is the latest on pypi... 
    try:
        pip_install("pymoose", version)
        pip_install("pint")
        import moose

        m = "Successfully installed MOOSE..."
    except Exception as e:
        m = "ERROR installing MOOSE: " + str(e)
    finally:
        print(m)
