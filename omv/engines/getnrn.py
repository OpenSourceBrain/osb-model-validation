from omv.common.inout import inform
from omv.common.inout import pip_install


def install_neuron(version):
    if not version:
        pip_install('neuron')
    else:
        pip_install(f'neuron=={version}')

    import neuron
    inform(f'Successfully installed NEURON v{version} using pip..', indent=2)
