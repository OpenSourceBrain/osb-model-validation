'''
Clone all OSB repos using OMV & test locally

'''

import sys
import os
import osb
import shutil
import datetime
import pprint

from subprocess import check_output as co
from omv.find_tests import test_all
from omv.backends.utils.wdir import working_dir

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

ignores = ['neurosciences-repository', 'brunel2000']

all_repos = {  }

additional_repos = { 'NeuroML2':             GitHubRepository.create('https://github.com/NeuroML/NeuroML2') ,
                     'osb-model-validation': GitHubRepository.create('https://github.com/OpenSourceBrain/osb-model-validation') }
                     
branches = { 'NeuroML2': 'development' }

all_repos.update(additional_repos)

projects = len(all_repos.keys())

if __name__ == "__main__":
    start = datetime.datetime.now()

    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_projects(min_curation_level="Low",
                                    limit=project_num):

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
                        print("That .travis.yml does not look like it uses OMV...")
                    else:
                        all_repos[project.identifier] = project.github_repo
                
            else:
                print("  (No GitHub repository)")
        else:
            print("  (Ignoring...)")
            
    pp.pprint(all_repos)
                
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
            print co(['git', 'clone', str(github_repo.clone_url), target_dir])
            
            with working_dir(target_dir):
                if proj_id in branches.keys():
                    print co(['git', 'checkout', branches[proj_id]])
                print "Running 'omv all' on", target_dir
                test_all()
            passing_projects += 1

            print("\nSo far: %i projects with OMV tests which pass\n" % (passing_projects))

    end = datetime.datetime.now()

    print("\n%i projects checked, of which %i have OMV tests (%i non-OMV tested projects) and %i passed with OMV in %s seconds\n" %
          (projects, testable_projects, non_omv_tests, passing_projects, (end - start).seconds))
