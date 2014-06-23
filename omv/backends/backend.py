from os.path import realpath

class BackendInstallationError(Exception):
    pass

class OMVBackend(object):

    def is_installed(self, version):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
    
    def install(self, version):
        raise NotImplementedError()

    def __init__(self, target, backend_version=None):
        if not self.is_installed(backend_version):
            try:
                self.install(backend_version)
            except: 
                raise(BackendInstallationError)

        self.modelpath = realpath(target)
        self.extra_pars = []



















