from os.path import realpath
from os import environ
import sys
from omv.common.inout import inform
import platform


class EngineInstallationError(Exception):
    pass


class EngineExecutionError(Exception):
    pass


class OMVEngine(object):

    name = 'Name not yet set!'
    environment_vars = {}
    path = ''
    
    python3_compatible = True # Most are so override only in those that aren't

    def __init__(self, target, do_not_check_install, engine_version=None):
        if not do_not_check_install:
            inform("Checking whether OMVEngine: %s (version: %s) is already installed..." % (self.name,
            engine_version if engine_version else 'DEFAULT'),
                   indent=1, verbosity=1)
            if not self.is_installed(engine_version):
                try:
                    if platform.python_version_tuple()[0]=='3' and \
                        not self.python3_compatible:
                        inform("Not installing %s due to Python 3 incompatibility. Tests will throw error unless option --ignore-non-py3 specified"%self.name)
                    else:
                        self.install(engine_version)
                        self.set_environment()
                        self.set_path()
                except Exception as e:
                    inform("Installation err: %s"%e)
                    raise(EngineInstallationError(e))
            '''
            if not self.is_installed(engine_version):  # Still
                inform("Fatal installation error for: %s"%self.name)
                exit(1)'''
            

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
            for name, val in self.environment_vars.items():
                if name in environ and not 'HOME' in name:
                    if not ':%s:'%val in environ[name]:
                        environ[name] = '%s:%s'%(environ[name],val)
                else:
                    environ[name] = val
                inform('Set env var %s: ' % name, environ[name],indent=2, verbosity=1)

    def set_path(self):
        if self.path:
            environ['PATH'] = ':'.join((environ['PATH'], self.path))
            inform('Setting PATH: ', environ['PATH'], indent=2, verbosity=1)

    def register_query(self, name, cmd=''):
        query = self.build_query_string(name, cmd)
        inform('Registered engine query: ', query, indent=2, verbosity=1)
        self.extra_pars.append(query)
        return name

    def fetch_query(self, key):
        import re
        match_float = '\s*([0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*'
        
        l = key+':' + match_float
        if sys.version_info[0]==3:
            l = l.encode()
        m = re.search(l, self.stdout)
        if m:
            return m.groups()[0]
        else:
            inform('Not found!')
            raise KeyError
