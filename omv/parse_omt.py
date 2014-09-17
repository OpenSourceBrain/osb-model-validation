from backends import OMVBackends
from omt_mep_parser import OMVTestParser
from common.io import inform


def parse_omt(omt_path):
    
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
    
    


