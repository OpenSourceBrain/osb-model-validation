from spikes import SpikeAnalyzer
from dryrun import DryRunAnalyzer
from resting import RestingAnalyzer
from morphology import MorphologyAnalyzer
from temperature import TemperatureAnalyzer
from activation import ActivationVariableAnalyzer
from input_resistance import InputResAnalyzer

OMVAnalyzers = {
    'spike times' : SpikeAnalyzer,
    'dry': DryRunAnalyzer,
    'resting': RestingAnalyzer,
    'morphology': MorphologyAnalyzer,
    'temperature': TemperatureAnalyzer,
    'activation variables': ActivationVariableAnalyzer,
    'input resistance': InputResAnalyzer
}

















