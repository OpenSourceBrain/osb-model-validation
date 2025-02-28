from omv.common.inout import pip_install

from omv.engines.getbrian1 import check_scipy_dev


def install_brian2(version):
    if not version:
        version = "2.5.3"
    try:
        pip_install("brian2", version)
        import brian2

        m = "Successfully installed Brian2 %s..."%brian2.__version__
    except Exception as e:
        m = "ERROR installing Brian2: " + str(e)
    finally:
        print(m)
