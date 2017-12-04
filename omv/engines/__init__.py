import inspect

from omv.engines.engine import OMVEngine
from omv.engines.neuron_ import NeuronEngine
from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.jneuromlnrn import JNeuroMLNRNEngine
from omv.engines.jneuromlpynnnrn import JNeuroMLPyNNNRNEngine
from omv.engines.jneuromlnetpyne import JNeuroMLNetPyNEEngine
from omv.engines.jneuromlnetpyne_np4 import JNeuroMLNetPyNENP4Engine
from omv.engines.jneuromlnetpyne_np2 import JNeuroMLNetPyNENP2Engine
from omv.engines.jneuromlbrian import JNeuroMLBrianEngine
from omv.engines.jneuromlbrian2 import JNeuroMLBrian2Engine
from omv.engines.jneuromlmoose import JNeuroMLMooseEngine
from omv.engines.jneuromlvalidate import JNeuroMLValidateEngine
from omv.engines.jneuromlvalidatev1 import JNeuroMLValidateV1Engine
from omv.engines.jlems import JLemsEngine
from omv.engines.pylems import PyLemsEngine
from omv.engines.pylemsnml2 import PyLemsNeuroML2Engine
from omv.engines.genesis import GenesisEngine
from omv.engines.brian1 import Brian1Engine
from omv.engines.brian2_ import Brian2Engine
from omv.engines.nestsli import NestEngine
from omv.engines.pynest import PyNestEngine
from omv.engines.moose_ import MooseEngine
from omv.engines.pynn import PyNNEngine
from omv.engines.pynnneuron import PyNNNRNEngine
from omv.engines.pyneuron import PyNRNEngine
from omv.engines.pynnbrian1 import PyNNBrian1Engine
from omv.engines.pynnnest import PyNNNestEngine
from omv.engines.pynnneuroml import PyNNNeuroMLEngine
from omv.engines.octave import OctaveEngine
from omv.engines.netpyne_ import NetPyNEEngine
from omv.engines.netpyne__np4 import NetPyNENP4Engine
from omv.engines.netpyne__np2 import NetPyNENP2Engine
from omv.engines.pyneuroconstruct import PyneuroConstructEngine
from omv.engines.pyneuroml_ import PyNeuroMLEngine


OMVEngines = {be.name: be for be in locals().values()
              if inspect.isclass(be)
              and issubclass(be, OMVEngine)
              and not be.name == 'Name not yet set!'}

