import os
import platform
from subprocess import check_output
from pathlib import Path

from omv.engines.utils.wdir import working_dir
from omv.common.inout import inform


def install_jnml(version):

    if not version:
        version = "v0.12.4"

    try:
        jnmlhome = os.environ["JNML_HOME"]
        jnmlpath = Path(jnmlhome).parent
    except KeyError:
        osname = platform.system()
        if osname == "Linux":
            try:
                jnmlpath = os.path.join(os.environ["XDG_DATA_HOME"], "jnml")
            except KeyError:
                localsharepath = os.path.join(os.environ["HOME"], ".local/share")
                if os.path.isdir(localsharepath):
                    jnmlpath = os.path.join(localsharepath, "jnml")
                else:
                    jnmlpath = os.path.join(os.environ["HOME"], "jnml")

        elif osname == "Darwin":
            jnmlpath = os.path.join(os.environ["HOME"], "Library/jnml")
        else:
            jnmlpath = os.path.join(os.environ["HOME"], "jnml")

    if not os.path.isdir(jnmlpath):
        os.mkdir(jnmlpath)
    with working_dir(jnmlpath):
        check_output(
            [
                "wget",
                "-nv",
                "https://github.com/NeuroML/jNeuroML/releases/download/%s/jNeuroML.zip"
                % (version),
            ]
        )
        check_output(["unzip", "jNeuroML.zip"])

    inform("Successfully installed jNeuroML "+version, indent=1)
