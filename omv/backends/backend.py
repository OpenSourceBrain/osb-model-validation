from os.path import realpath
from os import environ

class BackendInstallationError(Exception):
    pass

class OMVBackend(object):
    
    environment_vars = {}
    path = ''

    def is_installed(self, version):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
    
    def install(self, version):
        raise NotImplementedError()
        
    def set_environment(self):
        if self.environment_vars:
            for name,val in self.environment_vars.iteritems():
                environ[name] = val

    def set_path(self):
        if self.path:
            environ['PATH'] = ':'.join((environ['PATH'], self.path))
    
    def __init__(self, target, backend_version=None):
        
        
        if not self.is_installed(backend_version):
            try:
                self.install(backend_version)
                self.set_environment()
                self.set_path()
            except: 
                raise(BackendInstallationError)

        self.modelpath = realpath(target)
        self.extra_pars = []



















