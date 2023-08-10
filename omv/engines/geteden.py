from omv.common.inout import pip_install

DEFAULT_VERSION = "0.2.2"


def install_eden(version=None):
    if not version:
        version = DEFAULT_VERSION
    try:
        pip_install("eden-simulator", version)
        import eden_simulator

        m = "Successfully installed EDEN..."
    except Exception as e:
        m = "ERROR installing EDEN: " + str(e)
    finally:
        print(m)
