import yaml
import textwrap

LINEWIDTH = 70
PROMPT = '[omv] '


def omvify(x):
    return textwrap.TextWrapper(initial_indent=PROMPT,
                                subsequent_indent=PROMPT).fill(x)


def center(string):
    nwhite = (LINEWIDTH - len(PROMPT) - len(string)) // 2
    return nwhite * ' ' + string


def underlined(string, char='-'):
    rule = len(string) * char
    return map(center, [string, rule])


def inform(msg, pars=None, indent=0, underline=None):
    if underline:
        l = underlined(msg, underline)
        msg = '\n'.join(map(omvify, l))
    else:
        p = pars if pars else ''
        msg = omvify('  ' * indent + msg + p)
    print msg


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
