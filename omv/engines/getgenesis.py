import os
from subprocess import check_output as co

from omv.engines.utils.wdir import working_dir

simrc = """
// .simrc file to go in the home directory of all GENESIS users
//===========================================================================
//                         environment variables
//===========================================================================
//      SIMPATH - path to search for scripts (includes the startup path)
//      SIMNOTES - default file for simulator notes
//===========================================================================
setenv SIMPATH {getenv HOME}/genesis/genesis2.4gamma-master/src/startup \
{getenv HOME}/genesis/genesis2.4gamma-master/Scripts/neurokit \
{getenv HOME}/genesis/genesis2.4gamma-master/Scripts/neurokit/prototypes

// This adds the Xodus 1 compatability library directory to the
// SIMPATH.  If you are not expecting to use X1compat, you can
// comment out the following line.
setenv SIMPATH {getenv SIMPATH} \
{getenv HOME}/genesis/genesis2.4gamma-master/Scripts/X1compat

setenv SIMNOTES {getenv HOME}/genesis/genesis2.4gamma-master/.notes
setenv GENESIS_HELP {getenv HOME}/genesis/genesis2.4gamma-master/Doc

//===========================================================================
//                             set up tables 
//===========================================================================
schedule// default simulation schedule

// See /usr/genesis/startup/escapelist.g for macro definitions.  These allow
// you to use cursor keys for the recall and editing of previous commands
include          escapelist      // setup macro keys for DEC and SUN keyboards
"""


def install_genesis(get_latest=False):
    genpath = os.path.join(os.environ['HOME'], 'genesis')
    os.mkdir(genpath)
    with working_dir(genpath):
        print(co(['wget',
                  'https://github.com/borismarin/genesis2.4gamma/archive/master.zip']))
        print(co(['unzip', 'master.zip']))
        print(co(['ls', '-la', 'genesis2.4gamma-master']))
        os.chdir('genesis2.4gamma-master/src')
        print(co(['./configure']))
        print(co(['make']))
        open(os.path.join(os.environ['HOME'], '.simrc'), 'w').write(simrc)









