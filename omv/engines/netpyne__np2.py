import os
import subprocess as sp

from omv.engines.pyneuron import PyNRNEngine
from omv.engines.netpyne_ import NetPyNEEngine

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import EngineExecutionError

'''
    A temporary engine for testing running NetPyNE models in parallel mode.
    Would require update of NEURON installation process to ensure parallel 
    NEURON correctly installed, so mainly useful for local testing presently.
    Would also be better to incorporate this into netpyne_.py, and have correct 
    handling of variables specified in *.omt files
'''

class NetPyNENP2Engine(NetPyNEEngine):

    name = "NetPyNE_NP2"


    def run(self):


        try:
            self.stdout = PyNRNEngine.compile_modfiles(self.modelpath)
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)

        try:            
            inform("Running file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['mpiexec','-np','2','nrniv','-mpi', self.modelpath, '-nogui'],
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
















