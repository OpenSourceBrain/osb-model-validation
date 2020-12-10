import os
import subprocess as sp

from omv.engines.jneuromlnetpyne import JNeuroMLNetPyNEEngine

from omv.common.inout import inform, trim_path, check_output
from omv.engines.engine import EngineExecutionError

'''
    A temporary engine for testing running jNeuroML_NetPyNE models in parallel mode.
    Would require update of NEURON installation process to ensure parallel 
    NEURON correctly installed, so mainly useful for local testing presently.
    Would also be better to incorporate this into netpyne_.py, and have correct 
    handling of variables specified in *.omt files
'''

class JNeuroMLNetPyNENP4Engine(JNeuroMLNetPyNEEngine):

    name = "jNeuroML_NetPyNE_NP4"


    def run(self):

        np = 4

        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLNetPyNEEngine.name), indent=1)
            
            from omv.engines.jneuroml import JNeuroMLEngine
            jnml = JNeuroMLEngine.get_executable()
            self.stdout = check_output(
                [jnml, self.modelpath, '-netpyne', '-nogui', '-run', '-np', '%s'%np],
                cwd=os.path.dirname(self.modelpath),env=JNeuroMLEngine.get_environment())
            inform("Success with running ",
                   JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
