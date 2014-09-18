from backends import OMVBackends
from omt_mep_parser import OMVTestParser
from common.inout import inform
from os.path import basename


def parse_omt(omt_path):
    inform("Running tests defined in ", basename(omt_path),
           underline='=', center=True)
    
    mepomt = OMVTestParser(omt_path)
    backend = OMVBackends[mepomt.engine](mepomt.modelpath)
    experiments = [exp for exp in mepomt.generate_exps(backend)]

    backend.run()

    inform('running checks for experiments ',
           [exp.name for exp in experiments], indent=1)

    results = []
    for exp in experiments:
        results.append(exp.check_all)

    return results
    
    


