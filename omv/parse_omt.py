from omv.engines import OMVEngines
from omv.engines.engine import EngineInstallationError, EngineExecutionError
from omv.omt_mep_parser import OMVTestParser
from omv.common.inout import inform, check, trim_path
from omv.tally import Tallyman
import sys
import platform


def parse_omt(omt_path, do_not_run=False, engine_version=None, ignore_non_py3=False):
    inform('')
    action = 'Running'
    if do_not_run:
        action = 'Checking'
    inform(action+" the tests defined in ", trim_path(omt_path),
           underline='=', center=False)
    
    mepomt = OMVTestParser(omt_path)
    if not mepomt.engine in OMVEngines:
        inform("Error! Unrecognised engine: %s (try running: omv list-engines)"%mepomt.engine)
        exit(1)
    engine = OMVEngines[mepomt.engine](mepomt.modelpath, 
                                       do_not_check_install=do_not_run, 
                                       engine_version=engine_version)
                                       
    experiments = [exp for exp in mepomt.generate_exps(engine)]
    
    tally = Tallyman(mepomt)
    
    inform('Found %i experiment(s) to run on engine: %s '%(len(experiments), engine.name), indent=1)
    #print('%s, %s, %s'%(platform.python_version_tuple()[0],ignore_non_py3,engine.python3_compatible))
    
    if platform.python_version_tuple()[0]=='3' and \
       ignore_non_py3 and \
       not engine.python3_compatible:
           
        inform('Not running experiment(s) on: %s, as this is Python %s and engine is not Python 3 compatible...'%(engine.name, platform.python_version()), indent=1)
        tally.report_passing_if_no_exps = True
    
    elif not do_not_run:
        try:
            engine.run()
            some_failed = False
            for exp in experiments:
                inform('Running checks for experiment: ', exp.name, indent=1)
                inform('')
                results = exp.check_all()
                inform('{:<30}{:^20}'.format('Observable', 'Test Passed'),
                       underline='-', indent=3)
                for rn, rv in results.items():
                    if sys.version_info >= (3,0):
                        inform('{:<30}{:^20}'.format(rn, check(rv)), indent=3)
                    else:
                        inform(u'{:<30}{:^20}'.format(rn, check(rv)), indent=3)
                    if not rv:
                        some_failed = True
                tally.add_experiment(exp, results)

            if some_failed:
                inform("+++++++++++++++++++++ Error info ++++++++++++++++++", indent=3)
                inform(" Return code: %s"%engine.returncode, indent=3)
                if hasattr(engine,'stdout'):
                    if isinstance(engine.stdout, str):
                        out = engine.stdout
                    else:
                        out = str(engine.stdout.decode())
                    inform(" Output: %s"%out.replace('\n','\n[omv] %s:%s > '%(mepomt.omt_path,exp.name)), indent=3)
                inform("+++++++++++++++++++++++++++++++++++++++++++++++++++", indent=3)

        except (EngineInstallationError, EngineExecutionError):
            # TODO: serialize exception info
            inform('ERROR running engine ', engine.name, indent=1,
                   underline='-', overline='-')

    return tally
    
    


