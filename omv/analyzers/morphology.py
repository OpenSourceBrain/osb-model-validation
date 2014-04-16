from analyzer import OMVAnalyzer
from utils import timeseries as ts
from ..common.output import inform

class MorphologyAnalyzer(OMVAnalyzer):
    
    def before_running(self):
        if 'total area' in self.expected:
            base = self.observable.get('base section', 'cell[0]')
            self.query = self.backend.query_area(base)

    def parse_expected(self):
        return self.expected['total area']

    def parse_observable(self):
        return float(self.backend.fetch_query(self.query))


















