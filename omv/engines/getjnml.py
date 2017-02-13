import os
from subprocess import check_output as co

from omv.engines.utils.wdir import working_dir

def install_jnml():
    jnmlpath = os.path.join(os.environ['HOME'],'jnml')
    os.mkdir(jnmlpath)
    with working_dir(jnmlpath):
        print(co(['svn', 'checkout', 'https://svn.code.sf.net/p/neuroml/code/jNeuroMLJar']))
