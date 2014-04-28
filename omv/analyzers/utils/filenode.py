from timeseries import load_data_file

class FileNodeHelper(object):

    def __init__(self, fn):
        self.filename = fn['path']
        self.columns = fn.get('columns', (0,1))
        self.header = fn.get('header', 0)
        self.scaling = fn.get('scaling', (1,1))

    def __str__(self):
        return str({'file name' : str(self.filename),
            'columns (time, voltage)' : str(self.columns), 
            'initial rows to disregard' : str(self.header),
        })
    
    def get_timeseries(self):
        return load_data_file(self.filename, self.columns,
                              self.header, self.scaling)




















