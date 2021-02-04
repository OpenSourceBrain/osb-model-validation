import os
from subprocess import check_output

from omv.engines.utils.wdir import working_dir

def install_jnml():
        
    version='0.10.1'
    
    jnmlpath = os.path.join(os.environ['HOME'],'jnml')
    if not os.path.isdir(jnmlpath):
        os.mkdir(jnmlpath)
    with working_dir(jnmlpath):
        
        check_output(['wget', 'https://github.com/NeuroML/jNeuroML/releases/download/v%s/jNeuroML.zip'%(version)])
        check_output(['unzip', 'jNeuroML.zip'])
