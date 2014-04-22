osb-model-validation
====================

Tools for automated model validation in OpenSourceBrain projects.


Instructions
------------

Any _OSB_ project can have automated testing incorporated (currently,
only _LEMS_ and _NEURON_ implementations can be tested thoroughly,
though). In order to enable it:

- create a dry-run _Osb_ _Model_ _Test_ (_omt_) file, containing the
  target model file and the simulator, e.g.

    $echo -e "target: NeuroML2/LEMS_hh_nostim.xml \n engine: LEMS" > hh.omt

- copy the [travis template](templates/travis.yaml) to the projects' root dir,
  and rename it to *.travis.yml* (don't forget the leading dot!):

    $cd OSB_proj_dir
    $wget https://raw.githubusercontent.com/borismarin/osb-model-validation/master/templates/travis.yml.template
	$mv travis.yml.template .travis.yml


Once these changes are pushed to the _github_ repo, travis will run
the tests automatically. You can check the results at
http://travis-ci.org/OpenSourceBrain/project_name (and ideally add a
travis build badge to the projects' Readme.md file).


After this initial simple test passes, you can start writing more
elaborate tests by creating a _Model_ _Emergent_ _Properties_ (_mep_)
file and corresponding **O**SB **M**odel **T**est (_omt_) tests, as in
[](borismarin/hh-testing). _omt_ tests will be automatically
discovered independently of their location.
    

If you are wise a and want to run the tests locally, before submitting
your changes to github, install the omv python packacge

   $pip install git+https://github.com/borismarin/osb-model-validation.git

This package will provide three shell scripts:

- *omv_test* *[filename.omt]*, which runs a specific test locally

- *omv_alltests*, which recursively discovers all _.omt_ files in the
  project and runs them.

- *omv_validate_mep* *[filename.mep]*, to validate a _.mep_ file
  against the current _mep_ schema.


In other words, to run all _omt_ tests inside a project

   $cd OSB_proj_dir
   $omv_alltests
