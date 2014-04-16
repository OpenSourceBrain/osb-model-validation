from analyzer import OMVAnalyzer
from utils import timeseries as ts
from ..common.output import inform

class TemperatureAnalyzer(OMVAnalyzer):

    def before_running(self):
        self.query = self.backend.query_temperature()

    def parse_expected(self):
        return float(self.expected)

    def parse_observable(self):
        return float(self.backend.fetch_query(self.query))




