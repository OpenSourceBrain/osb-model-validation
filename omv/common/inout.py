import yaml
from collections import deque
# import textwrap

LINEWIDTH = 70
PROMPT = '[omv] '
INDENT = '  '
VERBOSITY = 0


def omvify(x):
    # return textwrap.TextWrapper(initial_indent=PROMPT,
    #                             subsequent_indent=len(PROMPT) * ' ',
    #                             replace_whitespace=False).fill(x)
    return PROMPT + x


def check(b):
    tick = u'\u2714' if b else u'\u2718'
    return tick


def centralize(string):
    fmt = '{{:^{}}}'.format(LINEWIDTH)
    return fmt.format(string)


def rule(string, char='-'):
    return len(string.lstrip()) * char


def inform(msg, pars=None, indent=0, underline=False,
           overline=False, center=False, verbosity=0):

    if verbosity > VERBOSITY:
        return

    if isinstance(msg, list):
        block = deque(msg)
        infostr = max(msg, key=len)
    else:
        p = pars if pars else ''
        infostr = msg + str(p)
        block = deque([infostr])

    if underline:
        block.append(rule(infostr, underline))
    if overline:
        block.appendleft(rule(infostr, overline))

    if center:
        block = map(centralize, block)
    if indent:
        block = map(lambda l: INDENT * indent + l, block)
          
    print '\n'.join(map(omvify, block))


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y
