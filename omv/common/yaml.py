import yaml


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
