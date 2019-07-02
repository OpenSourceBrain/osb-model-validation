from omv.analyzers.utils.timeseries import load_data_file, load_spike_file
from os.path import join, getmtime
from os.path import exists as os_exists


class FileNode(object):

    def get_timestamp(self):
        try:
            return getmtime(self.filename)
        except OSError:
            # No preexisting file
            return None

    def exists(self):
        return os_exists(self.filename)

    def has_changed(self):
        return self.get_timestamp() != self.tstamp


class FileNodeHelper(FileNode):

    def __init__(self, fn, root_dir):
        self.filename = join(root_dir, fn['path'])
        self.columns = fn.get('columns', (0, 1))
        self.header = fn.get('header', 0)
        self.scaling = fn.get('scaling', [1.]*len(self.columns))
        self.tstamp = self.get_timestamp()

    def get_timestamp(self):
        try:
            return getmtime(self.filename)
        except OSError:
            # No preexisting file
            return None

    def exists(self):
        return os_exists(self.filename)

    def has_changed(self):
        return self.get_timestamp() != self.tstamp

    def __str__(self):
        return str({'file name': str(self.filename),
                    'columns(time, voltage)': str(self.columns),
                    'initial rows to disregard': str(self.header)})
    
    def get_timeseries(self):
        return load_data_file(self.filename, self.columns,
                              self.header, self.scaling)


class SpikeFileNodeHelper(FileNode):

    def __init__(self, fn, root_dir):
        self.filename = join(root_dir, fn['path'])
        self.tstamp = self.get_timestamp()
        self.format = fn.get('format', 0)
        self.ids = fn.get('ids', 0)
        self.scaling = fn.get('scaling', 1)


    def __str__(self):
        return str({'spike file name': str(self.filename),
                    'format': str(self.format),
                    'ids': str(self.ids)})
    
    def get_spike_times(self):
        return load_spike_file(self.filename, self.format, self.ids, self.scaling)




















