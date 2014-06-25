import os
import subprocess as sp
from subprocess import check_output as co

from ..common.output import inform
from backend import OMVBackend

class JLemsBackend(OMVBackend):
    
    name = "jLEMS"

    @staticmethod
    def is_installed(version):
        print("Checking whether %s is installed..."%JLemsBackend.name)
        ret = True
        try:
            FNULL = open(os.devnull, 'w')
            sp.check_call(['lems', '-h'], stdout=FNULL)
        except OSError as err:
            print("Couldn't execute lems:\n%s"%err)
            ret = True
        return ret
        
    def install(self, version):
        from getjlems import install_jlems
        home = os.environ['HOME']
        p = os.path.join(home, 'jLEMS')
        self.path = p
        self.environment_vars = {'LEMS_HOME': p}
        inform('Will fetch and install the latest jLEMS', indent=2)
        install_jlems()
        inform('Done...', indent=2)
        

    def run(self):
        try:
            print("Running file %s with jLEMS" % self.modelpath)
            self.stdout = sp.check_output(['lems', self.modelpath, '-nogui'])
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
        except Exception as err:
            print("Another error with running jLEMS:\n%s"%err)
            self.returncode = -1
            self.stdout = "???"


















