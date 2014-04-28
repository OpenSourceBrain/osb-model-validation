from timeseries import load_data_file

class FileNodeHelper(object):

    def __init__(self, fn):
        self.filename = fn['path']
        self.columns = fn.get('columns', (0,1))
        self.header = fn.get('header', 0)

    def __str__(self):
        return '\n'.join([
            'file: ' + str(self.filename),
            'columns: ' + str(self.columns), 
            'header rows:' + str(self.header),
        ])

    def get_timeseries(self):
        return load_data_file(self.filename, self.columns, self.header)
















