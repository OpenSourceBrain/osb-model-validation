from neuron import NeuronBackend
from jneuroml import JNeuroMLBackend
from jneuromlnrn import JNeuroMLNRNBackend
from jlems import JLemsBackend

OMVBackends = {
    NeuronBackend.name : NeuronBackend,
    JNeuroMLBackend.name : JNeuroMLBackend,
    JNeuroMLNRNBackend.name : JNeuroMLNRNBackend,
    JLemsBackend.name : JLemsBackend
}
