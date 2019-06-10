from omv.analyzers.spikes import SpikeAnalyzer
from omv.analyzers.rates import RateAnalyzer
from omv.analyzers.dryrun import DryRunAnalyzer
from omv.analyzers.resting import RestingAnalyzer
from omv.analyzers.morphology import MorphologyAnalyzer
from omv.analyzers.temperature import TemperatureAnalyzer
from omv.analyzers.activation import ActivationVariableAnalyzer
from omv.analyzers.input_resistance import InputResAnalyzer
from omv.analyzers.timeseries import TimeSeriesAnalyzer

OMVAnalyzers = {
    'spike times' : SpikeAnalyzer,
    'spike rate' : RateAnalyzer,
    'dry': DryRunAnalyzer,
    'resting': RestingAnalyzer,
    'morphology': MorphologyAnalyzer,
    'temperature': TemperatureAnalyzer,
    'activation variables': ActivationVariableAnalyzer,
    'input resistance': InputResAnalyzer,
    'timeseries': TimeSeriesAnalyzer
}

















