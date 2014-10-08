import yaml
from collections import deque
import os
# import textwrap

LINEWIDTH = 70
__PROMPT__ = '[omv] '
__INDENT__ = '  '
__VERBOSITY__ = 0


def omvify(x):
    # return textwrap.TextWrapper(initial_indent=__PROMPT__,
    #                             subsequent_indent=len(__PROMPT__) * ' ',
    #                             replace_whitespace=False).fill(x)
    return __PROMPT__ + x


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

    if verbosity > __VERBOSITY__:
        return

    if isinstance(msg, list):
        block = deque(msg)
        infostr = max(msg, key=len)
    else:
        p = pars if pars else ''
        #print("msg is %s"%msg.__class__)
        msgstr = msg.encode('utf-8') if isinstance(msg, unicode) else str(msg)
        infostr = msgstr + str(p)
        block = deque([infostr])

    if underline:
        block.append(rule(infostr, underline))
    if overline:
        block.appendleft(rule(infostr, overline))

    if center:
        block = map(centralize, block)
    if indent:
        block = map(lambda l: __INDENT__ * indent + l, block)
          
    print '\n'.join(map(omvify, block))


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y


def trim_path(fname):
    cwd = os.getcwd()
    if fname.startswith(cwd):
        return "."+fname[len(cwd):]
    else:
        return fname
