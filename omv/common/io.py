import yaml


def inform(msg, pars=[], indent=0):
    p = pars if (pars is not None and pars != []) else ''
    print 'OMV >>>  ' + '    ' * indent + msg, p


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
