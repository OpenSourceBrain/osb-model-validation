from os.path import realpath
from os import environ
from ..common.inout import inform


class BackendInstallationError(Exception):
    pass


class OMVBackend(object):

    name = 'Name not yet set!'
    environment_vars = {}
    path = ''

    def __init__(self, target, backend_version=None):
        inform("Checking whether %s is installed..." % self.name,
               indent=1, verbosity=1)
        if not self.is_installed(backend_version):
            try:
                self.install(backend_version)
                self.set_environment()
                self.set_path()
            except Exception as e:
                inform(e)
                raise(BackendInstallationError)

        self.modelpath = realpath(target)
        self.extra_pars = []

    def __str__(self):
        return self.name

    def is_installed(self, version):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def install(self, version):
        raise NotImplementedError()
        
    def build_query_string(self, name, cmd):
        raise NotImplementedError()

    def set_environment(self):
        if self.environment_vars:
            for name, val in self.environment_vars.iteritems():
                inform('Setting env var %s: ' % name, val,
                       indent=2, verbosity=1)
                environ[name] = val

    def set_path(self):
        if self.path:
            environ['PATH'] = ':'.join((environ['PATH'], self.path))
            inform('Setting path', environ['PATH'], indent=2, verbosity=1)

    def register_query(self, name, cmd=''):
        query = self.build_query_string(name, cmd)
        inform('Registered backend query: ', query, indent=2, verbosity=1)
        self.extra_pars.append(query)
        return name

    def fetch_query(self, key):
        import re
        match_float = '\s*([0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*'
        m = re.search(key+':' + match_float, self.stdout)
        if m:
            return m.groups()[0]
        else:
            inform('Not found!')
            raise KeyError
