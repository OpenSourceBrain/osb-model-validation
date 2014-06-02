from neuron import NeuronBackend
from lems import LemsBackend

OMVBackends = {
    'NEURON' : NeuronBackend,
    'jNeuroML' : LemsBackend
}

be_paths = {'NEURON': "$HOME/neuron/nrn/`arch`/bin",
            'jNeuroML': "$HOME/jnml/jNeuroMLJar"}
be_env_vars = {'jNeuroML':"JNML_HOME=$HOME/jnml/jNeuroMLJar"}
