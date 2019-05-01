import os
import subprocess as sp

from omv.engines.pyneuroml_ import PyNeuroMLEngine

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError


class MooseEngine(OMVEngine):
    
    name = "Moose"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether the engine %s has been installed correctly..." %
                   MooseEngine.name, indent=1)
    
        ret = True
        try:
            
            ret_str = sp.check_output(['python -c "import moose; print(moose.__version__)"'], shell=True,stderr=sp.STDOUT)
            ret = len(ret_str) > 0
            
            if ret and is_verbose():
                inform("%s is correctly installed..." % (MooseEngine.name), indent=2)
            if ret:    
                import moose
                ret = 'v%s'%moose.__version__
            
        except Exception as err:
            inform("Couldn't import moose into Python: ", err, indent=1)
            ret = False
        if not ret or not PyNeuroMLEngine.is_installed(None):
            ret = False
        
        inform("Moose is_installed(): %s"%ret, "", indent=1, verbosity=2)
        return ret
        
    @staticmethod
    def install(version):
        
        if not PyNeuroMLEngine.is_installed(None):
            PyNeuroMLEngine.install(None)
            inform("%s installed PyNeuroML..." % MooseEngine.name, indent=2, verbosity =1)
            
        from omv.engines.getmoose import install_moose
        home = os.environ['HOME']
        inform('Will fetch and install the latest Moose..', indent=2)
        install_moose()
        inform('Done, Moose is correctly installed...', indent=2)


    def run(self):
        
        
        try:            
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, '-nogui'],
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
















