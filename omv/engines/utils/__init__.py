from omv.engines.engine import PATH_DELIMITER


def resolve_paths(path_s):
    """
    Make explicit list from: '*.nml myfile.xml' etc.
    """

    if "*" in path_s:
        import glob

        if PATH_DELIMITER in path_s:
            all = []
            for p in path_s.split(PATH_DELIMITER):
                for g in glob.glob(p):
                    all.append(g)
            path_s = all
        else:
            path_s = glob.glob(path_s)

    return path_s
