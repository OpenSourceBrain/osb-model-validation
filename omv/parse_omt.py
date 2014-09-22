from backends import OMVBackends
from backends.backend import BackendInstallationError, BackendExecutionError
from omt_mep_parser import OMVTestParser
from common.inout import inform, check
from os.path import basename
from tally import Tallyman


def parse_omt(omt_path):
    inform('')
    inform("Running tests defined in ", basename(omt_path),
           underline='=', center=False)
    
    mepomt = OMVTestParser(omt_path)
    backend = OMVBackends[mepomt.engine](mepomt.modelpath)
    experiments = [exp for exp in mepomt.generate_exps(backend)]
    
    tally = Tallyman(mepomt)
    
    try:
        backend.run()
        for exp in experiments:
            inform('Running checks for experiment ', exp.name, indent=1)
            inform('')
            results = exp.check_all()
            inform('{:<30}{:^20}'.format('Observable', 'Test Passed'),
                   underline='-', indent=3)
            for rn, rv in results.iteritems():
                inform(u'{:<30}{:^20}'.format(rn, check(rv)), indent=3)
            tally.add_experiment(exp, results)

    except (BackendInstallationError, BackendExecutionError):
        # TODO: serialize exception info
        inform('ERROR running backend ', backend.name, indent=1,
               underline='-', overline='-')

    return tally
    
    


