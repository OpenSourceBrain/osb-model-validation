"""OpenSourceBrain Model Validation and Testing
============================================

  Usage:
    omv all [-V | --verbose] [--engine=engine] [--ignore-non-py3]
    omv all_ [-V | --verbose] [--engine=engine]
    omv test <testMe.omt> [-V | --verbose]
    omv autogen [options]
    omv install <engine>
    omv find
    omv (list-engines | list) [-V | --verbose]
    omv validate-mep <mepfile>
    omv validate-omt <omtfile>
    omv (-h | --help)
    omv --version

  Options:
    -h --help         Show this screen.
    -d --dryrun       Generate dry-run tests only [default: False].
    -V --verbose      Display additional diagnosis messages [default: False].
    --version         Show version.
    --ignore-non-py3  If Python 3, ignore tests on non Py3 compatible engines [default: False]
    -y                Auto-select default options (non-interactive mode)
"""

from docopt import docopt
from omv.find_tests import test_all, test_one
from omv.validation import validate_mep
from omv.autogen import autogen
from omv.engines import OMVEngines
from omv.common.inout import inform
import os
import platform

from omv.common.inout import set_verbosity

from omv import __version__ as omv_version


def main():
    arguments = docopt(
        __doc__, version="OpenSourceBrain Model Validation %s" % omv_version
    )
    set_env_vars()

    if arguments["--verbose"]:
        set_verbosity(1)

    if arguments["test"]:
        try:
            test_one(arguments["<testMe.omt>"])
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    elif arguments["all"]:
        try:
            if platform.python_version_tuple()[0] == "3":
                inform(
                    "Python 3. Ignoring tests for non Py3 compatible engines: %s"
                    % arguments["--ignore-non-py3"]
                )

            if arguments["--engine"] is not None:
                if ":" in arguments["--engine"]:
                    _install_engine(arguments["--engine"])
                only_this_engine = arguments["--engine"].split(":")[0]
            else:
                only_this_engine = None

            test_all(
                only_this_engine=only_this_engine,
                ignore_non_py3=arguments["--ignore-non-py3"],
            )
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    # Includes *.omt_, i.e. temporary test files
    elif arguments["all_"]:
        try:
            test_all(
                only_this_engine=arguments["--engine"],
                include_temp_tests=True,
                ignore_non_py3=arguments["--ignore-non-py3"],
            )
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    elif arguments["find"]:
        try:
            test_all(do_not_run=True)
        except AssertionError:
            inform("Failed due to non passing tests")
            exit(1)

    elif arguments["validate-mep"]:
        validate_mep.validate(arguments["<mepfile>"])

    elif arguments["validate-omt"]:
        inform("OMT validation not implemented yet!")
        exit(1)

    elif arguments["install"]:
        set_verbosity(1)
        eng = arguments["<engine>"]

        _install_engine(eng)

    elif arguments["list-engines"] or arguments["list"]:
        inform("OMV is checking which engines are currently installed...")
        set_verbosity(0)  # No need to report failures
        engines = sorted(OMVEngines.keys())

        installed = {}
        for engine in engines:
            installed[engine] = OMVEngines[engine].is_installed()

        inform("")
        inform(
            "The following engines are currently supported by OMV (v%s):" % omv_version
        )
        inform("")
        for engine in engines:
            py3_info = (
                "" if OMVEngines[engine].python3_compatible else "; non Py3 compatible"
            )
            inform(
                "  %s%s(installed: %s%s)"
                % (engine, " " * (30 - len(engine)), installed[engine], py3_info)
            )
        inform("")
        if arguments["--verbose"]:
            inform("Additional Python (v%s) packages:" % platform.python_version())
            inform("")
            for m in [
                "matplotlib",
                "numpy",
                "pandas",
                "scipy",
                "sympy",
                "tables",
                "h5py",
                "neo",
                "lazyarray",
                "pyelectro",
                "neurotune",
                "lems",
                "pyneuroml",
                "neuroml",
                "neuromllite",
                "libsbml",
            ]:
                installed_ver = False
                try:
                    mod = __import__(m)
                    installed_ver = "v%s" % getattr(mod, "__version__", "unknown")
                except Exception:
                    pass
                inform(
                    "  %s%s(installed: %s)" % (m, " " * (30 - len(m)), installed_ver)
                )
            inform("")

    elif arguments["autogen"]:
        inform("Automatically generating model validation files")
        dry = arguments["--dryrun"]
        auto = arguments["-y"]
        autogen(auto, dry)


def _install_engine(eng):
    engine_version = None

    if ":" in eng:
        ee = eng.split(":")
        eng = ee[0]
        engine_version = ee[1]
        inform("Engine %s version %s will be used..." % (eng, engine_version))
    else:
        inform("Engine %s, default version will be used..." % (eng))

    if eng.lower() not in [e.lower() for e in OMVEngines]:
        inform("Engine " + eng + " unknown!")
    else:
        inform("Trying to install: %s" % eng)
        already_installed = False

        if eng.lower() == "NEURON".lower():
            from omv.engines.neuron_ import NeuronEngine

            if not NeuronEngine.is_installed():
                from omv.engines.getnrn import install_neuron

                install_neuron(engine_version)
            else:
                already_installed = True

        elif eng.lower() == "PyNEURON".lower():
            from omv.engines.pyneuron import PyNRNEngine

            if not PyNRNEngine.is_installed():
                from omv.engines.getnrn import install_neuron

                install_neuron(engine_version)
            else:
                already_installed = True

        elif eng.lower() == "jLEMS".lower():
            from omv.engines.jlems import JLemsEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                if engine_version is not None:
                    raise Exception(
                        "Currently, cannot install a specific version of engine %s"
                        % eng
                    )
                from omv.engines.getjlems import install_jlems

                install_jlems()

        elif eng.lower() == "jNeuroML".lower():
            from omv.engines.jneuroml import JNeuroMLEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getjnml import install_jnml

                install_jnml(engine_version)

        elif eng.lower() == "neuroConstruct" or eng == "Py_neuroConstruct".lower():
            from omv.engines.pyneuroconstruct import PyneuroConstructEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                if engine_version is not None:
                    raise Exception(
                        "Currently, cannot install a specific version of engine %s"
                        % eng
                    )
                from omv.engines.getneuroconstruct import install_neuroconstruct

                install_neuroconstruct()

        elif eng.lower() == "pyNeuroML".lower():
            from omv.engines.pyneuroml_ import PyNeuroMLEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                ee.install(engine_version)

        elif eng.lower() == "PyLEMS".lower():
            from omv.engines.pylems import PyLemsEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                if engine_version is not None:
                    raise Exception(
                        "Currently, cannot install a specific version of engine %s"
                        % eng
                    )
                from omv.engines.getpylems import install_pylems

                install_pylems()

        elif eng.lower() == "Arbor".lower():
            from omv.engines.arbor_ import ArborEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getarbor import install_arbor

                install_arbor(engine_version)

        elif eng.lower() == "XPP".lower():
            from omv.engines.xpp import XppEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getxpp import install_xpp

                install_xpp(engine_version)

        elif eng.lower() == "EDEN".lower():
            from omv.engines.eden_ import EdenEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.geteden import install_eden

                install_eden(engine_version)

        elif eng.lower() == "PyLEMS_NeuroML2".lower():
            pylems_already_installed = False
            nml2_already_installed = False

            from omv.engines.pylems import PyLemsEngine as ee

            if ee.is_installed():
                pylems_already_installed = True
            else:
                from omv.engines.getpylems import install_pylems

                install_pylems()

            from omv.engines.getnml2 import install_nml2, is_nml2_installed

            if is_nml2_installed():
                nml2_already_installed = True
            else:
                if engine_version is not None:
                    raise Exception(
                        "Currently, cannot install a specific version of engine %s"
                        % eng
                    )
                install_nml2()

            already_installed = nml2_already_installed and pylems_already_installed

        elif eng.lower() == "Py_neuroConstruct".lower():
            from omv.engines.pyneuroconstruct import PyneuroConstructEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                if engine_version is not None:
                    raise Exception(
                        "Currently, cannot install a specific version of engine %s"
                        % eng
                    )
                from omv.engines.getneuroconstruct import install_neuroconstruct

                install_neuroconstruct()

        elif eng.lower() == "genesis".lower():
            if engine_version is not None:
                raise Exception(
                    "Currently, cannot install a specific version of engine %s" % eng
                )
            from omv.engines.getgenesis import install_genesis

            install_genesis()

        elif eng.lower() == "Moose".lower():
            from omv.engines.moose_ import MooseEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getmoose import install_moose

                install_moose(engine_version)

        elif eng.lower() == "NetPyNE".lower():
            from omv.engines.getnetpyne import install_netpyne

            install_netpyne(engine_version)

        elif eng.lower() == "Brian".lower():
            if engine_version is not None:
                raise Exception(
                    "Currently, cannot install a specific version of engine %s" % eng
                )
            from omv.engines.getbrian1 import install_brian

            install_brian()

        elif eng.lower() == "Brian2".lower():
            from omv.engines.brian2_ import Brian2Engine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getbrian2 import install_brian2

                install_brian2(engine_version)

        elif eng.lower() == "NEST".lower():
            from omv.engines.nestsli import NestEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getnest import install_nest

                install_nest(engine_version)

        elif eng.lower() == "PyNEST".lower():
            from omv.engines.pynest import PyNestEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                from omv.engines.getnest import install_nest

                install_nest(engine_version)
        elif eng.lower() == "PyNN".lower():
            from omv.engines.getpynn import install_pynn

            install_pynn(engine_version)

        elif eng.lower() == "PyNN_NEURON".lower():
            if engine_version is not None:
                raise Exception(
                    "Currently, cannot install a specific version of engine %s" % eng
                )
            from omv.engines.pynnneuron import PyNNNRNEngine

            PyNNNRNEngine.install()

        elif eng.lower() == "jNeuroML_Brian2".lower():
            from omv.engines.jneuromlbrian2 import JNeuroMLBrian2Engine as ee

            if ee.is_installed():
                already_installed = True
            else:
                ee.install(engine_version)

        elif eng.lower() == "jNeuroML_Moose".lower():
            from omv.engines.jneuromlmoose import JNeuroMLMooseEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                ee.install(engine_version)

        elif eng.lower() == "jNeuroML_NEURON".lower():
            from omv.engines.jneuromlnrn import JNeuroMLNRNEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                ee.install(engine_version)

        elif eng.lower() == "jNeuroML_EDEN".lower():
            from omv.engines.jneuromleden import JNeuroMLEdenEngine as ee

            if ee.is_installed():
                already_installed = True
            else:
                ee.install(engine_version)

        else:
            inform(
                "Code not implemented yet for installing %s using: omv install! Try running a test using this engine."
                % eng
            )
            exit(1)
        if already_installed:
            inform("Engine %s was already installed" % eng)


def set_env_vars():
    if os.name == "nt":
        # Windows does not have a HOME var defined by default
        os.environ["HOME"] = os.environ["USERPROFILE"]


if __name__ == "__main__":
    main()
