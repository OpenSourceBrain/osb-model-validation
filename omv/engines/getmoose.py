from omv.common.inout import pip_install


def install_moose(version):
    if not version:
        version = "4.1.2"
    try:
        pip_install("pint") # Ensure pint is installed first
        pip_install("pymoose", version)
        import moose

        m = "Successfully installed MOOSE..."
    except Exception as e:
        m = "ERROR installing MOOSE: " + str(e)
    finally:
        print(m)
