'''
Clone all OSB repos using OMV & test locally

'''   

        
import sys
import osb

testable_projects = 0
passing_projects = 0
projects = 0


if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_projects(min_curation_level="Low", limit=project_num):

        print("\n%sProject: %s (%s)\n" % ("-"*8,project.name,project.identifier))

        github_repo = project.github_repo

	projects +=1
	passed = 1


	if github_repo is not None:
            identifier = project.identifier

	    if github_repo.check_file_in_repository(".travis.yml"):
                print("  .travis.yml found!")
                testable_projects +=1

            else:
		    print("  (No .travis.yml)")

	else:
	    print("  (No GitHub repository)")




    print("\nNumber of projects: %i, of which %i have tests and %i passed\n"%(projects, testable_projects, passing_projects))

