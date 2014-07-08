import inspect

from backend import OMVBackend
from neuron import NeuronBackend
from jneuroml import JNeuroMLBackend
from jneuromlnrn import JNeuroMLNRNBackend
from jlems import JLemsBackend
from genesis import GenesisBackend

OMVBackends = {be.name:be for be in locals().values()
              if inspect.isclass(be)
              and issubclass(be, OMVBackend)}

