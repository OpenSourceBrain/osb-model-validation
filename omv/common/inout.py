import os

# import textwrap
import subprocess as sp
from collections import deque

import yaml

LINEWIDTH = 70
__PROMPT__ = "[omv] "
__INDENT__ = "  "
__VERBOSITY__ = 0


def set_verbosity(v):
    global __VERBOSITY__
    __VERBOSITY__ = v


def omvify(x):
    # return textwrap.TextWrapper(initial_indent=__PROMPT__,
    #                             subsequent_indent=len(__PROMPT__) * ' ',
    #                             replace_whitespace=False).fill(x)
    return __PROMPT__ + x


def check(b):
    tick = "\u2714" if b else "\u2718"
    return tick


def centralize(string):
    fmt = "{{:^{}}}".format(LINEWIDTH)
    return fmt.format(string)


def rule(string, char="-"):
    return len(string.lstrip()) * char


def is_verbose(level=1):
    return __VERBOSITY__ >= level


def inform(
    msg, pars=None, indent=0, underline=False, overline=False, center=False, verbosity=0
):
    if verbosity > __VERBOSITY__:
        return

    if isinstance(msg, list):
        block = deque(msg)
        infostr = max(msg, key=len)
    else:
        p = pars if pars else ""
        # print("msg is %s"%msg.__class__)
        msgstr = str(msg)
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

    print("\n".join(map(omvify, block)))


def load_yaml(fname):
    with open(fname) as f:
        y = yaml.safe_load(f)
    return y


def trim_path(fname):
    cwd = os.getcwd()
    if fname.startswith(cwd):
        return "." + fname[len(cwd) :]
    else:
        return fname


def check_output(cmds, cwd=".", shell=False, verbosity=0, env=None):
    inform(
        "Running the commands: [%s] in (%s; cwd=%s; shell=%s; env=%s)"
        % (" ".join(cmds), cwd, os.getcwd(), shell, env),
        indent=2,
        verbosity=verbosity,
    )
    joint_env = {}
    if env:
        joint_env.update(env)
    for k in os.environ:
        if k not in joint_env:
            joint_env[k] = os.environ[k]

    try:
        ret_string = sp.check_output(
            cmds, cwd=cwd, shell=shell, env=joint_env, stderr=sp.STDOUT
        )
        inform(
            "Commands: %s completed successfully" % (cmds),
            indent=2,
            verbosity=verbosity,
        )
        if isinstance(ret_string, bytes):
            ret_string = ret_string.decode("utf-8")  # For Python 3...
        return ret_string

    except sp.CalledProcessError as err:
        inform("Error: %s" % (err), indent=2, verbosity=verbosity)
        raise err
    except Exception as err:
        inform("Error: %s" % (err), indent=2, verbosity=verbosity)
        raise err


def pip_install(packages, version=None):
    pip = "pip"
    cmds = [pip, "install"]
    if isinstance(packages, str):
        if version is None:
            cmds.append(packages)
        else:
            cmds.append("%s==%s" % (packages, version))
    else:
        raise Exception("pip_install will only install single packages...")
        """
        for p in packages:
            cmds.append(p)"""
    print(check_output(cmds))
