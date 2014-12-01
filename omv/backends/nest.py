import os
import subprocess as sp

from ..common.inout import inform, trim_path, check_output
from backend import OMVBackend, BackendExecutionError


class NestBackend(OMVBackend):
    
    name = "NEST"
    

    @staticmethod
    def is_installed(version):
        ret = True
        
        nestpath2 = os.path.join(os.environ['HOME'],'nest/nest')
        try:
            FNULL = open(os.devnull, 'w')
            print(check_output([nestpath2+'/bin/nest', '-v']))
        except OSError as err:
            inform("Couldn't execute NEST: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from getnest import install_nest
        home = os.environ['HOME']
        p = os.path.join(home, 'nest')
        NestBackend.path = p
        NestBackend.environment_vars = {'NEST_HOME': p}
        inform('Will fetch and install the latest NEST', indent=2)
        install_nest()
        inform('Done...', indent=2)
        
    def run(self):
        
        nestpath2 = os.path.join(os.environ['HOME'],'nest/nest')
        
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = sp.check_output([nestpath2+'/bin/nest', self.modelpath],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise BackendExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"


















