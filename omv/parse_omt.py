from engines import OMVEngines
from engines.engine import EngineInstallationError, EngineExecutionError
from omt_mep_parser import OMVTestParser
from common.inout import inform, check, trim_path
from tally import Tallyman


def parse_omt(omt_path, do_not_run=False):
    inform('')
    action = 'Running'
    if do_not_run:
        action = 'Checking'
    inform(action+" tests defined in ", trim_path(omt_path),
           underline='=', center=False)
    
    mepomt = OMVTestParser(omt_path)
    if not OMVEngines.has_key(mepomt.engine):
        inform("Error! Unrecognised engine: %s (try running: omv find-engines)"%mepomt.engine)
        exit(1)
    engine = OMVEngines[mepomt.engine](mepomt.modelpath, do_not_run)
    experiments = [exp for exp in mepomt.generate_exps(engine)]
    
    tally = Tallyman(mepomt)
    
    inform('Found %i experiment(s) to run on engine: %s '%(len(experiments), engine.name), indent=1)
    
    if not do_not_run:
        try:
            engine.run()
            for exp in experiments:
                inform('Running checks for experiment: ', exp.name, indent=1)
                inform('')
                results = exp.check_all()
                inform('{:<30}{:^20}'.format('Observable', 'Test Passed'),
                       underline='-', indent=3)
                for rn, rv in results.iteritems():
                    inform(u'{:<30}{:^20}'.format(rn, check(rv)), indent=3)
                tally.add_experiment(exp, results)

        except (EngineInstallationError, EngineExecutionError):
            # TODO: serialize exception info
            inform('ERROR running engine ', engine.name, indent=1,
                   underline='-', overline='-')

    return tally
    
    


