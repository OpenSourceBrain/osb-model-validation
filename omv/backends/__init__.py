from neuron import NeuronBackend
from jneuroml import JNeuroMLBackend
from jlems import JLemsBackend

OMVBackends = {
    'NEURON' : NeuronBackend,
    'jNeuroML' : JNeuroMLBackend,
    'jLEMS' : JLemsBackend
}

be_paths = {'NEURON': "$HOME/neuron/nrn/`arch`/bin",
            'jNeuroML': "$HOME/jnml/jNeuroMLJar",
            'jNeuroML': "$HOME/jLEMS"}
            
be_env_vars = {'jNeuroML':"JNML_HOME=$HOME/jnml/jNeuroMLJar",
               'jLEMS':"LEMS_HOME=$HOME/jLEMS"}
