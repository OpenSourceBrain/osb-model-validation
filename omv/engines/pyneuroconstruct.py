import os

from omv.engines.utils.wdir import working_dir

from omv.common.inout import inform, check_output as co, trim_path
from omv.engines.engine import OMVEngine


class PyneuroConstructEngine(OMVEngine):
    
    name = "Py_neuroConstruct"
    
    @staticmethod
    def get_nC_environment():

        nc_path = os.path.join(os.environ['HOME'],'neuroConstruct')
        if 'NC_HOME' in os.environ:
            nc_path = os.environ['NC_HOME']+'/'

        environment_vars = {'NC_HOME': nc_path}

        return environment_vars

    @staticmethod
    def is_installed(version):
        nChome = PyneuroConstructEngine.get_nC_environment()['NC_HOME']
        inform('Checking whether neuroConstruct is installed (in %s)'%nChome, indent=2, verbosity=2)
        ret = True
        try:
            with working_dir(nChome):
                r = co(['./nC.sh','-v'], verbosity=1)
                ret = 'v%s'%r.split('neuroConstruct, version: ')[-1].split()[0]
        except Exception as err:
            inform("Couldn't execute neuroConstruct:", err, indent=1)
            ret = False
        return ret
        
        
    @staticmethod
    def install(version):

        from omv.engines.getneuroconstruct import install_neuroconstruct
        
        inform('Will fetch and install the latest neuroConstruct', indent=2)
        install_neuroconstruct()
        inform('Done...', indent=2)


    def run(self):
        
        try:
            inform("Running file %s with Py_neuroConstruct" % trim_path(self.modelpath), indent=1)
            
            nC_sh = os.path.join(PyneuroConstructEngine.get_nC_environment()['NC_HOME'], 'nC.sh')
            self.stdout = co([nC_sh, '-python', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except Exception as err:
            inform("Error with running Py_neuroConstruct:", err, indent=1)
            self.returncode = -1
            self.stdout = "???"
















