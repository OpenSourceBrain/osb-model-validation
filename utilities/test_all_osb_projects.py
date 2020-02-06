'''
Clone all OSB repos using OMV & test locally

'''

import sys
import os
import osb
import shutil
import datetime
import pprint
import sys

from subprocess import check_output as co
from omv.find_tests import test_all
from omv.engines.utils.wdir import working_dir

from osb.Repository import GitHubRepository

testable_projects = 0
non_omv_tests = 0
passing_projects = 0

pp = pprint.PrettyPrinter(indent=4)

test_dir = "local_test"

fresh_clones = True

if fresh_clones:
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

os.makedirs(test_dir)

ignores = ['neurosciences-repository', 'drosophila-acc-l3-motoneuron-gunay-et-al-2014','d-olfactory-bulb-network','zetterbergjansenritmodel','test_net']

if '-q' in sys.argv:
    ignores.append('pospischiletal2008')  # Slow...
    ignores.append('blue-brain-project-showcase')  # Slow...
    ignores.append('acnet2')  # Slow...
    ignores.append('granulecell')  # Slow...
    ignores.append('thalamocortical')  # Slow...
    ignores.append('cerebellum--cerebellar-golgi-cell--solinasetal-golgicell')  # Slow...
    ignores.append('potjansdiesmann2014') 
    ignores.append('nc_ca1')
    ignores.append('miglioreetal14_olfactorybulb3d')
    ignores.append('sadehetal2017-inhibitionstabilizednetworks')

ignores.append('l23dendriticspikes')
#ignores.append('izhikevichmodel')
ignores.append('ionl-testing')
ignores.append('test')
ignores.append('salomon-muller')
ignores.append('slow-oscillation')
ignores.append('swrs')

all_repos = {  }

additional_repos = { 'NeuroML2':             GitHubRepository.create('https://github.com/NeuroML/NeuroML2') ,
                     'osb-model-validation': GitHubRepository.create('https://github.com/OpenSourceBrain/osb-model-validation') }
                     
branches = { 'neuroml2': 'development', 'nc_ca1': 'development' }

all_repos.update(additional_repos)

projects = len(all_repos.keys())

bad_projects_found = {}

if __name__ == "__main__":
    start = datetime.datetime.now()

    project_num = 1000
    if len(sys.argv) == 2:
        try:
            project_num = int(sys.argv[1])
        except:
            print("ignoring...")
            
    all_projs = osb.get_projects(min_curation_level="None",
                                    limit=project_num)
            
    for project in all_projs:

        print("\n%sPre checking OSB project: %s (%s)\n" %
              ("-" * 8, project.name, project.identifier))
        
        if project.identifier not in ignores:

            github_repo = project.github_repo

            projects += 1

            if github_repo is not None:
                
                if github_repo.check_file_in_repository(".travis.yml"):

                    raw_url = github_repo.link_to_raw_file_in_repo(".travis.yml")
                    print("  .travis.yml found at %s\n" % raw_url)
                    contents = osb.utils.get_page(raw_url)
                    if 'omv' not in contents:
                        error = "  (That .travis.yml does not look like it uses OMV...)"
                        print(error)
                        
                        bad_projects_found[project.identifier] = error
                    else:
                        print("  Possible .travis.yml with OMV tests found!")
                        all_repos[project.identifier] = project.github_repo
                        
                else:
                    error = "  (No .travis.yml)"
                    print(error)

                    bad_projects_found[project.identifier] = error
                        
                
            else:
                error = "  (No GitHub repository)"
                print(error)
                bad_projects_found[project.identifier] = error
        else:
            error = "  (Ignoring...)"
            print(error)
            bad_projects_found[project.identifier] = error
          
    print("\nFound %i/%i projects with possible OMV tests"%(len(all_repos),len(all_projs)))
    pp.pprint(all_repos)
    print("\nFound %i/%i projects without OMV tests"%(len(bad_projects_found),len(all_projs)))
    pp.pprint(bad_projects_found)
    
                
    for proj_id in all_repos.keys():
        
        github_repo = all_repos[proj_id]
        
        test_it = False
        
        print("\n%sChecking project: %s (%s)\n" %
              ("-" * 8, proj_id, github_repo))
        
        if proj_id in additional_repos.keys():
            test_it = True
            testable_projects += 1

        elif github_repo.check_file_in_repository(".travis.yml"):

            raw_url = github_repo.link_to_raw_file_in_repo(".travis.yml")
            print("  .travis.yml found at %s\n" % raw_url)
            contents = osb.utils.get_page(raw_url)
            if 'omv' not in contents:
                print("That .travis.yml does not look like it uses OMV...")
                non_omv_tests += 1
            else:
                testable_projects += 1
                test_it = True

        else:
            print("  (No .travis.yml)")
            
        if test_it:
            target_dir = '%s/%s' % (test_dir, proj_id)
            print(co(['git', 'clone', str(github_repo.clone_url), target_dir]))
            
            with working_dir(target_dir):
                for key in branches.keys():
                    if proj_id.lower() == key: 
                        print(co(['git', 'checkout', branches[key]]))
                print("Running 'omv all' on"+ target_dir)
                test_all()
            passing_projects += 1

            print("\nSo far: %i projects with OMV tests which pass\n" % (passing_projects))

    end = datetime.datetime.now()

    print("\n%i projects checked, of which %i have OMV tests (%i non-OMV tested projects) and %i passed with OMV in %s seconds\n" %
          (projects, testable_projects, non_omv_tests, passing_projects, (end - start).seconds))
