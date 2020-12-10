[![Build Status](https://travis-ci.com/OpenSourceBrain/osb-model-validation.svg?branch=master)](https://travis-ci.com/OpenSourceBrain/osb-model-validation)
------------------------------------------


OSB Model Validation
====================

Tools for automated model validation in [Open Source Brain](http://www.opensourcebrain.org) projects, but which can be used for testing model behaviour on many simulation engines, both locally and on [Travis-CI](https://travis-ci.com).

To see this framework in action, click on some of the green buttons below:   

|  OSB project   |   Tests on Travis-CI    |  .travis.yml script |
|----------|:-------------:|:------:|
|[FitzHugh Nagumo](http://www.opensourcebrain.org/projects/fitzhugh-nagumo-fitzhugh-1969) | [![Build Status](https://travis-ci.com/OpenSourceBrain/FitzHugh-Nagumo.svg?branch=master)](https://travis-ci.com/OpenSourceBrain/FitzHugh-Nagumo) | [.travis.yml](https://github.com/borismarin/FitzHugh-Nagumo/blob/master/.travis.yml) |
|[Auditory cortex network](http://www.opensourcebrain.org/projects/acnet2)|[![Build Status](https://travis-ci.com/OpenSourceBrain/ACnet2.svg?branch=master)](https://travis-ci.com/OpenSourceBrain/ACnet2)|[.travis.yml](https://github.com/OpenSourceBrain/ACnet2/blob/master/.travis.yml)|
| [SBML Showcase](http://www.opensourcebrain.org/projects/sbmlshowcase) | [![Build Status](https://travis-ci.com/OpenSourceBrain/SBMLShowcase.svg?branch=master)](https://travis-ci.com/OpenSourceBrain/SBMLShowcase) | [.travis.yml](https://github.com/OpenSourceBrain/SBMLShowcase/blob/master/.travis.yml)|

This framework has been used to test the 25+ NeuroML and PyNN models described in the [Open Source Brain paper (Gleeson et al. 2019)](https://www.cell.com/neuron/fulltext/S0896-6273(19)30444-1). 

Installation
------------

Quick install:
 
    sudo pip install git+https://github.com/OpenSourceBrain/osb-model-validation
    
Install from cloned repository:

    git clone https://github.com/OpenSourceBrain/osb-model-validation.git
    cd osb-model-validation
    sudo python setup.py install 

Instructions
------------

Any _OSB_ project can have automated testing incorporated. For an overview of the various OSB projects with OMV tests, see https://travis-ci.org/OpenSourceBrain (note not all of these use OMV yet).

In order to enable it:

- create a dry-run <b>O</b>SB <b>M</b>odel <b>T</b>est (_omt_) file, containing the
  target model file and the simulator, e.g.
 
      echo -e "target: LEMS_hh_nostim.xml\nengine: LEMS" > NeuroML2/hh.omt
 

- copy the [travis config file template](templates/travis.yml.template) to the projects' root dir,
  and rename it to *.travis.yml* (don't forget the leading dot!):

      cd OSB_proj_dir
      wget https://raw.githubusercontent.com/borismarin/osb-model-validation/master/templates/travis.yml.template
      mv travis.yml.template .travis.yml


Once these changes are pushed to the _github_ repo, travis will run
the tests automatically. You can check the results at
http://travis-ci.com/OpenSourceBrain/project_name (and ideally add a
travis build badge to the projects' Readme.md file). Check 
[this project](https://github.com/borismarin/hh-testing) for a working example. 


After this initial simple test passes, you can start writing more
elaborate tests by creating a <b>M</b>odel <b>E</b>mergent <b>P</b>roperties (_mep_)
file and corresponding _omt_ tests. Examples of supported constructs can be found [here]
(https://github.com/borismarin/hh-testing). Notice that _omt_ tests will
be automatically discovered by travis, _regardless_ of their location.
    

If you are wise and want to run the tests locally before submitting
your changes to github, install the omv python package

    pip install git+https://github.com/OpenSourceBrain/osb-model-validation.git

This package provides the *omv* command line utility:

- *omv test <filename.omt>*, which runs a specific test locally

- *omv all*, which recursively discovers all _.omt_ files in the
  project and runs them (this is the command used by travis).

- *omv validate_mep <filename.mep>*, to validate a _.mep_ file
  against the current _mep_ schema.

- additional options: ```omv -h```

        OpenSourceBrain Model Validation and Testing
        ============================================
        
        Usage:
          omv all [-V | --verbose]
          omv test <testMe.omt> [-V | --verbose]
          omv autogen [options]
          omv install <backend>
          omv list-backends
          omv validate-mep <mepfile>
          omv validate-omt <omtfile>
          omv (-h | --help)
          omv --version
      
        Options:
          -h --help     Show this screen.
          -d --dryrun   Generate dry-run tests only [default: False].
          -V --verbose  Display additional diagnosis messages [default: False].
          --version     Show version.
          -y            Auto-select default options (non-interactive mode)

Evidently, we will provide a *validate_omt* script as soon as we agree on 
its schema.

In other words, to run all _omt_ tests inside a project: 

    cd OSB_proj_dir
    omv all
