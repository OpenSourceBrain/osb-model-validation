import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError


class NestEngine(OMVEngine):

    name = "NEST"


    @staticmethod
    def get_nest_environment():

        nestpath = os.path.join(os.environ['HOME'],'nest/nest/')
        if 'NEST_INSTALL_DIR' in os.environ:
            nestpath = os.environ['NEST_INSTALL_DIR']+'/'

        environment_vars = {'NEST_HOME': nestpath,
                            'PYTHONPATH': nestpath+'/lib/python2.7/site-packages/'}

        return environment_vars


    @staticmethod
    def is_installed(version):
        ret = True

        environment_vars = NestEngine.get_nest_environment()
        try:
            FNULL = open(os.devnull, 'w')

            r = check_output([environment_vars['NEST_HOME']+'bin/nest', '-v'], verbosity=2)
    
            ret = '%s'%r.split('version')[1].split()[0][:-1]
            if '-' in ret:
                ret = 'v%s'%ret.split('-')[-1]
                
            inform("NEST %s is correctly installed..." % ret, indent=2, verbosity=1)
            
        except OSError as err:
            inform("Couldn't execute NEST: ", err, indent=1)
            ret = False
        return ret


    @staticmethod
    def install(version):

        from omv.engines.getnest import install_nest
        install_nest(version)
        inform('Done...', indent=2)


    def run(self):

        self.environment_vars = NestEngine.get_nest_environment()
        self.set_environment()

        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output([self.environment_vars['NEST_HOME']+'bin/nest', self.modelpath],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"


