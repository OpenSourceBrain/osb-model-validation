from engines import OMVEngines
from engines.engine import EngineInstallationError, EngineExecutionError
from omt_mep_parser import OMVTestParser
from common.inout import inform, check, trim_path
from tally import Tallyman


def parse_omt(omt_path):
    inform('')
    inform("Running tests defined in ", trim_path(omt_path),
           underline='=', center=False)
    
    mepomt = OMVTestParser(omt_path)
    if not OMVEngines.has_key(mepomt.engine):
        inform("Error! Unrecognised engine: %s"%mepomt.engine)
        exit(1)
    engine = OMVEngines[mepomt.engine](mepomt.modelpath)
    experiments = [exp for exp in mepomt.generate_exps(engine)]
    
    tally = Tallyman(mepomt)
    
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
    
    


