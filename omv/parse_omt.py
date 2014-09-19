from backends import OMVBackends
from backends.backend import BackendInstallationError, BackendExecutionError
from omt_mep_parser import OMVTestParser
from common.inout import inform, check
from os.path import basename


def parse_omt(omt_path):
    inform('')
    inform("Running tests defined in ", basename(omt_path),
           underline='=', center=False)
    
    mepomt = OMVTestParser(omt_path)
    backend = OMVBackends[mepomt.engine](mepomt.modelpath)
    experiments = [exp for exp in mepomt.generate_exps(backend)]
    
    results = [False]
    try:
        backend.run()
        results = []
        for exp in experiments:
            inform('Running checks for experiment ', exp.name, indent=1)
            inform('')
            res = exp.check_all()
            results.append(res.values)
            inform('{:<30}{:^20}'.format('Observable', 'Test Passed'),
                   underline='-', indent=3)
            for rn, rv in res.iteritems():
                inform(u'{:<30}{:^20}'.format(rn, check(rv)), indent=3)
    except (BackendInstallationError, BackendExecutionError):
        inform('ERROR running backend ', backend.name, indent=1,
               underline='-', overline='-')

    return results
    
    


