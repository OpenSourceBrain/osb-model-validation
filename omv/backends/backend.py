from os.path import realpath
from os import environ

class BackendInstallationError(Exception):
    pass


class OMVBackend(object):

    name = 'Name not yet set!'
    environment_vars = {}
    path = ''

    def __init__(self, target, backend_version=None):
        if not self.is_installed(backend_version):
            try:
                self.install(backend_version)
                self.set_environment()
                self.set_path()
            except Exception as e:
                print(e)
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
                print '\t Setting env var', name, '=', val
                environ[name] = val

    def set_path(self):
        if self.path:
            environ['PATH'] = ':'.join((environ['PATH'], self.path))
            print '\t Setting path', environ['PATH']

    def register_query(self, name, cmd=''):
        query = self.build_query_string(name, cmd) 
        print '\t\tRegistered backend query:', query
        self.extra_pars.append(query)
        return name

    def fetch_query(self, key):
        import re
        m = re.search(key+':'+'\s*([0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*', self.stdout)
        if m:
            return m.groups()[0]
        else:
            print 'not found!'
            raise KeyError
