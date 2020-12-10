import os
import subprocess as sp

from omv.common.inout import inform, trim_path, is_verbose, check_output
from omv.engines.engine import OMVEngine, EngineExecutionError


class JNeuroMLEngine(OMVEngine):

    name = "jNeuroML"
    
    @staticmethod
    def get_environment():

        if 'JNML_HOME' in os.environ:
            jnmlhome = os.environ['JNML_HOME']
        else:
            jnmlhome = os.path.join(os.environ['HOME'],'jnml/jNeuroMLJar')
        
        environment_vars = {'JNML_HOME': jnmlhome}

        return environment_vars
    
    @staticmethod
    def get_executable():
        
        environment_vars = JNeuroMLEngine.get_environment()
        jnml = os.path.join(environment_vars['JNML_HOME'],'jnml' if os.name != 'nt' else 'jnml.bat')
        return jnml
        
    @staticmethod
    def is_installed(version):
        ret = True
        try:
            if is_verbose():
                inform("Checking whether %s is installed..." %
                   JNeuroMLEngine.name, indent=1)
            FNULL = open(os.devnull, 'w')
            jnml = JNeuroMLEngine.get_executable()
            r = check_output([jnml, '-v'], verbosity=2,
                                          env=JNeuroMLEngine.get_environment())
            ret = '%s'%r.split()[1]
            
            if is_verbose():
                inform("%s %s is installed..." %
                       (JNeuroMLEngine.name, ret), indent=2)
        except OSError as err:
            inform("Couldn't execute/import jNeuroML: ", err, indent=1)
            ret = False
        return ret
        
    @staticmethod
    def install(version):
        from omv.engines.getjnml import install_jnml
     
        inform('Will fetch and install the latest jNeuroML jar', indent=2)
        install_jnml()

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name),
                   indent=1)
            
            jnml = JNeuroMLEngine.get_executable()
            self.stdout = sp.check_output([jnml, self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath),
                                          env=JNeuroMLEngine.get_environment())
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
