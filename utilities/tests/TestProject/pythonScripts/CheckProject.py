# -*- coding: utf-8 -*-
#
#   File to test configuration/default parameters in ACnet2 project
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

import sys
import os

try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using 'nC.bat -python XXX.py' or 'nC.sh -python XXX.py'"
    print "which use Jython (and so can access the Java classes in nC), as opposed to standard C based Python"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.neuron import NeuronSettings


projFile = File("../TestProject.ncx")



def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()
    
    projectManager = ProjectManager()
    project = projectManager.loadProject(projFile)

    assert(len(project.getProjectDescription())>0)

    assert(len(project.cellManager.getAllCells())>=1)

    #assert(project.proj3Dproperties.getDisplayOption() == Display3DProperties.DISPLAY_SOMA_SOLID_NEURITE_LINE)

    assert(abs(project.simulationParameters.getDt()-0.02)<=1e-9)
    
    assert(abs(project.simulationParameters.getTemperature() - 6.3) < 1e-6)

    assert(not project.neuronSettings.isVarTimeStep())

    assert(project.neuronSettings.getDataSaveFormat().equals(NeuronSettings.DataSaveFormat.TEXT_NC))

    assert(project.genesisSettings.isSIUnits())
    
    defSimConfig = project.simConfigInfo.getSimConfig("Default Simulation Configuration")
    assert(str(defSimConfig.getCellGroups())=='[SampleCellGroup]')
    
    assert(defSimConfig.getCellGroups().size()==1)
    
    assert(defSimConfig.getInputs().size()==1)
    

    print "\n**************************************"
    print "    All tests passed!"
    print "**************************************\n"

if __name__ == "__main__":
    testAll()
    exit()
