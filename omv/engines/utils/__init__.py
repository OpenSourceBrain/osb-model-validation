from omv.engines.engine import PATH_DELIMITER


def resolve_paths(path_s):
    """
    Make explicit list from: '*.nml myfile.xml' etc.
    """

    import glob

    if PATH_DELIMITER in path_s:
        all_paths = []
        for p in path_s.split(PATH_DELIMITER):
            for g in glob.glob(p):
                print('Found path:', g)
                all_paths.append(g)
        path_s = all_paths
    else:
        path_s = resolve_paths(glob.glob(path_s))

    return path_s
