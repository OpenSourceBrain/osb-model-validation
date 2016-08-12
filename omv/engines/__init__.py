import inspect

from engine import OMVEngine
from neuron_ import NeuronEngine
from jneuroml import JNeuroMLEngine
from jneuromlnrn import JNeuroMLNRNEngine
from jneuromlpynnnrn import JNeuroMLPyNNNRNEngine
from jneuromlnetpyne import JNeuroMLNetPyNEEngine
from jneuromlbrian import JNeuroMLBrianEngine
from jneuromlvalidate import JNeuroMLValidateEngine
from jneuromlvalidatev1 import JNeuroMLValidateV1Engine
from jlems import JLemsEngine
from pylems import PyLemsEngine
from pylemsnml2 import PyLemsNeuroML2Engine
from genesis import GenesisEngine
from brian1 import Brian1Engine
from brian2_ import Brian2Engine
from nestsli import NestEngine
from pynest import PyNestEngine
from pynn import PyNNEngine
from pynnneuron import PyNNNRNEngine
from pyneuron import PyNRNEngine
from pynnbrian1 import PyNNBrian1Engine
from pynnnest import PyNNNestEngine
from octave import OctaveEngine
from netpyne_ import NetPyNEEngine
from pyneuroconstruct import PyneuroConstructEngine


OMVEngines = {be.name: be for be in locals().values()
              if inspect.isclass(be)
              and issubclass(be, OMVEngine)
              and not be.name == 'Name not yet set!'}

