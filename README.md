[![Continuous builds](https://github.com/OpenSourceBrain/osb-model-validation/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenSourceBrain/osb-model-validation/actions/workflows/ci.yml)
------------------------------------------


# OSB Model Validation

Tools for automated model validation in [Open Source Brain](http://www.opensourcebrain.org) projects, which can also be used for testing model behaviour on many simulation engines locally and on [GitHub Actions](https://github.com/features/actions).

To see this framework in action, click on some of the green buttons below:

|  OSB project   |   Tests on GitHub Actions    |  Test workflow script |
|----------|:-------------:|:------:|
|[FitzHugh Nagumo](http://www.opensourcebrain.org/projects/fitzhugh-nagumo-fitzhugh-1969) | [![Continuous build using OMV](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/actions/workflows/omv-ci.yml/badge.svg)](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/actions/workflows/omv-ci.yml) | [omv-ci.yml](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/blob/master/.github/workflows/omv-ci.yml) |
|[Auditory cortex network](http://www.opensourcebrain.org/projects/acnet2)| [![Continuous build using OMV](https://github.com/OpenSourceBrain/ACnet2/actions/workflows/omv-ci.yml/badge.svg)](https://github.com/OpenSourceBrain/ACnet2/actions/workflows/omv-ci.yml) | [omv-ci.yml](https://github.com/OpenSourceBrain/ACnet2/blob/master/.github/workflows/omv-ci.yml) |
| [SBML Showcase](http://www.opensourcebrain.org/projects/sbmlshowcase)| [![Continuous build using OMV](https://github.com/OpenSourceBrain/sbmlshowcase/actions/workflows/omv-ci.yml/badge.svg)](https://github.com/OpenSourceBrain/sbmlshowcase/actions/workflows/omv-ci.yml) | [omv-ci.yml](https://github.com/OpenSourceBrain/sbmlshowcase/blob/master/.github/workflows/omv-ci.yml) |

This framework has been used to test the 25+ NeuroML and PyNN models described in the [Open Source Brain paper (Gleeson et al. 2019)](https://www.cell.com/neuron/fulltext/S0896-6273(19)30444-1), and [many more](https://github.com/OpenSourceBrain/.github/blob/main/testsheet/README.md).

Note: [Travis-CI](https://travis-ci.com) is no longer the preferred testing platform due to limitations with number of free test runs. 

## Installation

Quick system-wide install:

``` bash
sudo pip install git+https://github.com/OpenSourceBrain/osb-model-validation
```

System-wide install from cloned repository:

``` bash
git clone https://github.com/OpenSourceBrain/osb-model-validation.git
cd osb-model-validation
sudo python setup.py install
```

If you'd like to install only in a virtual environment in the `.venv` directory:

``` bash
git clone https://github.com/OpenSourceBrain/osb-model-validation.git
cd osb-model-validation

# Create the virtual environment
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
python setup.py install

# To deactivate the virtual environment:
deactivate
```

## Instructions

Any _Open Source Brain_ project can have automated testing incorporated.
For an overview of the various Open Source Brain projects with OMV tests, see https://github.com/OpenSourceBrain/.github/blob/main/testsheet/README.md (note not all of these use OMV yet).

Setting up validation for a model and simulation written in NeuroML2/LEMS requires two additional steps:

- write a <b>M</b>odel <b>E</b>mergent <b>P</b>roperties (_mep_) file.
- write the corresponding <b>O</b>SB <b>M</b>odel <b>T</b>est (_omt_) file.


### Write MEP files

Depending on the size of your model, you can run validation on the full fledged model, or you can create smaller stripped down versions that test particular aspects of the model.
Here is an example LEMS file for the FitzHugh-Nagumo model on Open Source Brain: [LEMS_FitzHugNagamo.xml](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/blob/master/NeuroML2/LEMS_FitzHughNagumo.xml).

``` yaml
# Script for running automated tests on OSBrain, see https://github.com/OpenSourceBrain/osb-model-validation

system: The Fitzhugh-Nagumo model, classical parameters

experiments:
  experiment 1, free run:
    expected:
      spike times: [2.24, 39.82, 76.53, 113.24, 149.94, 186.65, 223.36, 260.07, 296.78, 333.49, 370.2]
```

MEP files include information on what is expected from the simulation run.
OMV will run the simulation based on the OMT files (which we'll see below), and compare the output to the information provided in MEP files.
Multiple _experiments_ can be mentioned in the MEP file, and each project can have multiple MEP files.

The MEP file for the FitzHugh-Nagumo model is [here](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/blob/master/fhn.mep).
It includes a single experiment, with the expected spike times that the simulation run should generate.

### Writing OMT files

OMT files include information on simulating the model for validation.
The FitzHugh-Nagumo model on Open Source Brain includes multiple OMT files that can be seen [here](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/tree/master/NeuroML2).

- Each OMT file specifies a _target_ file, which is the LEMS simulation file to be run.

- Each OMT file specifies an _engine_ that OMV supports.
    Engines are simulators that OMV should use to run the model.
    For example, the [.test.fhn.jnml.omt](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/blob/master/NeuroML2/.test.fhn.jnml.omt) file uses the `jNeuroML` engine, which implies that the model should be run using plain jNeuroML (and not any of the simulators that jNeuroML supports, like NEURON).

``` yaml
# Script for running automated tests on OSB, see https://github.com/OpenSourceBrain/osb-model-validation

target: LEMS_FitzHughNagumo.xml
engine: jNeuroML
mep: ../fhn.mep
experiments:
  experiment 1, free run:
    observables:
      spike times:
        file:
          path: ./fhn.dat
          columns: [0,1]
          scaling: [1000, 1]
        spike detection:
          method: derivative
        tolerance: 2.185696883946938e-16
```

- Each OMT file specifies the MEP file that the output of its simulation run should be compared to.
    In this case, we use the same MEP file for all OMT files.

- Finally, like MEP files, OMT files also include _experiments_.
    The names of the experiments in the OMT files must correspond to those used in the MEP files, so that OMV knows what section of the OMT and MEP files are related to each other.
    In each experiment, we specify our _observables_, which are to be compared to the information provided in the MEP file.
    Here, we inform OMV that we are observing _spike times_, which will be recorded by the simulation run in `fhn.dat`.
    We also inform OMV what columns of this file the information is to be extracted from, and if these columns need to be scaled before they are compared to the data provided in the MEP file.
    Finally, while simulations can save spike times directly and OMV will compare these to the MEP file, if the simulation is recording membrane potentials, OMV can also be asked to detect spikes from this data using the _spike detection_ section.
    The _tolerance_ key tells OMV what the acceptable difference between the expected and observed data values is.

This is the OMT file to validate the same model using the `jNeuroML_NEURON` engine: [.test.fhn.jnmlnrn.omt](https://github.com/OpenSourceBrain/FitzHugh-Nagumo/blob/master/NeuroML2/.test.fhn.jnmlnrn.omt).
It uses the same MEP file, and observes the same recorded information.
It only tells OMV to use a different simulation engine:

``` yaml
# Script for running automated tests on OSB, see https://github.com/OpenSourceBrain/osb-model-validation

target: LEMS_FitzHughNagumo.xml
engine: jNeuroML_NEURON
mep: ../fhn.mep
experiments:
  experiment 1, free run:
    observables:
      spike times:
        file:
          path: ./fhn.dat
          columns: [0,1]
          scaling: [1000, 1]
        spike detection:
          method: derivative
        tolerance: 0
```
### Running validation tests locally

If you have installed OMV successfully, you can now run all the OMV tests locally, by running this command:

    omv all

Learn more about the options `omv` can take by running `omv --help`.

Running validation tests locally ensures that you can quickly check if any changes you have made to the model cause changes to its specific outcomes.
Since you can run the validation with different engines to use different simulators, this also allows you to quickly verify that your model gives similar results using these different tools.


### Running tests automatically on ~~Travis-CI~~

**Note: Travis-CI is no longer the preferred platform for testing, [GitHub Actions](https://github.com/features/actions) is. To use OMV with GHA, copy an existing configuration file, e.g. https://github.com/OpenSourceBrain/ACnet2/blob/master/.github/workflows/omv-ci.yml**


