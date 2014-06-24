from neuron import NeuronBackend
from jneuroml import JNeuroMLBackend
from jneuromlnrn import JNeuroMLNRNBackend
from jlems import JLemsBackend

OMVBackends = {
    'NEURON' : NeuronBackend,
    'jNeuroML' : JNeuroMLBackend,
    'jNeuroML_NEURON' : JNeuroMLNRNBackend,
    'jLEMS' : JLemsBackend
}

be_paths = {'NEURON': "$HOME/neuron/nrn/`arch`/bin",
            'jNeuroML': "$HOME/jnml/jNeuroMLJar",
            'jNeuroML_NEURON': "$HOME/jnml/jNeuroMLJar",
            'jLEMS': "$HOME/jLEMS"}
            
be_env_vars = {'jNeuroML':"JNML_HOME=$HOME/jnml/jNeuroMLJar",
               'jNeuroML_NEURON':"JNML_HOME=$HOME/jnml/jNeuroMLJar",
               'jLEMS':"LEMS_HOME=$HOME/jLEMS"}
