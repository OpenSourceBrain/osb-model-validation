import yaml
import textwrap

LINEWIDTH = 70
PROMPT = '[omv] '
INDENT = '  '


def omvify(x):
    return textwrap.TextWrapper(initial_indent=PROMPT,
                                subsequent_indent=PROMPT,
                                replace_whitespace=False).fill(x)


def centralize(string):
    nwhite = (LINEWIDTH - len(PROMPT) - len(string))//2 
    return nwhite * ' ' + string


def rule(string, char='-'):
    return len(string) * char


def inform(msg, pars=None, indent=0, underline=False, overline=False, center=False):
    p = pars if pars else ''
    infostr = INDENT * indent + msg + p
    if underline:
        block = [infostr, rule(infostr, underline)]
    elif overline:
        block = [rule(infostr, overline), infostr]
    else:
        block = [infostr]
    if center:
        block = map(centralize, block)
    print '\n'.join(map(omvify, block))


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
