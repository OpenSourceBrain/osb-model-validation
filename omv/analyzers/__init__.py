from spikes import SpikeAnalyzer
from dryrun import DryRunAnalyzer
from resting import RestingAnalyzer
from morphology import MorphologyAnalyzer
from temperature import TemperatureAnalyzer

OMVAnalyzers = {
    'spike times' : SpikeAnalyzer,
    'dry': DryRunAnalyzer,
    'resting': RestingAnalyzer,
    'morphology': MorphologyAnalyzer,
    'temperature': TemperatureAnalyzer
}

















