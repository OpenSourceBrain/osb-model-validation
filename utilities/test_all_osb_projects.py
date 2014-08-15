'''
Clone all OSB repos using OMV & test locally

'''   

        
import sys
import os
import osb
import shutil
import datetime
from subprocess import check_output as co

projects = 0
testable_projects = 0
non_omv_tests = 0
passing_projects = 0

test_dir = "local_test"

fresh_clones = True

if fresh_clones: 
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
os.makedirs(test_dir)

if __name__ == "__main__":
    start = datetime.datetime.now()

    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_projects(min_curation_level="Low", limit=project_num):

        print("\n%sProject: %s (%s)\n" % ("-"*8,project.name,project.identifier))

        github_repo = project.github_repo

        projects +=1


        if github_repo is not None:
            identifier = project.identifier

            if github_repo.check_file_in_repository(".travis.yml"):

                raw_url = github_repo.link_to_raw_file_in_repo(".travis.yml")
                print("  .travis.yml found at %s\n"%raw_url)
                contents = osb.utils.get_page(raw_url)
                if not 'omv' in contents:
                    print("That .travis.yml does not look like it uses OMV...")
                    non_omv_tests+=1
                else:
                    testable_projects +=1
                    target_dir = '%s/%s'%(test_dir, project.identifier)
                    print co(['git', 'clone', project.github_repo_str, target_dir])
                    print co(['omv', 'all'], cwd=target_dir)
                    passing_projects +=1

            else:
                print("  (No .travis.yml)")

        else:
            print("  (No GitHub repository)")



    end = datetime.datetime.now()

    print("\n%i projects checked, of which %i have OMV tests (%i non-OMV tested projects) and %i passed with OMV in %s seconds\n"%(projects, testable_projects, non_omv_tests, passing_projects, (end-start).seconds))

