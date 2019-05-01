import os
import subprocess as sp

from omv.common.inout import inform, trim_path, is_verbose, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError


class JNeuroMLEngine(OMVEngine):

    name = "jNeuroML"
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            if is_verbose():
                inform("Checking whether %s is installed..." %
                   JNeuroMLEngine.name, indent=1)
            FNULL = open(os.devnull, 'w')
            r = check_output(['jnml' if os.name != 'nt' else 'jnml.bat', '-v'], verbosity=2)
            ret = '%s'%r.split()[1]
        except OSError:
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from omv.engines.getjnml import install_jnml
        home = os.environ['HOME']
        p = os.path.join(home, 'jnml/jNeuroMLJar')
        JNeuroMLEngine.path = p
        JNeuroMLEngine.environment_vars = {'JNML_HOME': p}
        inform('Will fetch and install the latest jNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name),
                   indent=1)
            self.stdout = sp.check_output(['jnml' if os.name != 'nt' else 'jnml.bat', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
