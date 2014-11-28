import inspect

from backend import OMVBackend
from neuron import NeuronBackend
from jneuroml import JNeuroMLBackend
from jneuromlnrn import JNeuroMLNRNBackend
from jneuromlbrian import JNeuroMLBrianBackend
from jneuromlvalidate import JNeuroMLValidateBackend
from jneuromlvalidatev1 import JNeuroMLValidateV1Backend
from jlems import JLemsBackend
from pylems import PyLemsBackend
from pylemsnml2 import PyLemsNeuroML2Backend
from genesis import GenesisBackend
from brian1 import Brian1Backend
from pynn import PyNNBackend


OMVBackends = {be.name: be for be in locals().values()
              if inspect.isclass(be)
              and issubclass(be, OMVBackend)}

