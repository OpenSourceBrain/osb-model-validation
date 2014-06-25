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

be_paths = {NeuronBackend.name: "$HOME/neuron/nrn/`arch`/bin",
            JNeuroMLBackend.name: "$HOME/jnml/jNeuroMLJar",
            JNeuroMLNRNBackend.name: "$HOME/jnml/jNeuroMLJar:$HOME/neuron/nrn/`arch`/bin",
            JLemsBackend.name: "$HOME/jLEMS"}
            
be_env_vars = {JNeuroMLBackend.name:"JNML_HOME=$HOME/jnml/jNeuroMLJar",
               'jNeuroML_NEURON':"JNML_HOME=$HOME/jnml/jNeuroMLJar",
               JLemsBackend.name:"LEMS_HOME=$HOME/jLEMS"}
