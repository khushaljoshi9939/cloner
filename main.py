import os
import constants
import helper
import sys

# queue will be processed based on groups
# this will ensure parent will be processed and then child
queue = []

def start(rootGroupId, rootGroupName, username, accessToken):

    # initial queue setup
    queue = helper.getSubGroups(rootGroupId, accessToken, constants.CURRENT_PATH / rootGroupName)
    projects = helper.getProjects(rootGroupId, accessToken)

    for project in projects:
        projectGitUrl = project["http_url_to_repo"]
        ProjectGitUrlWithAuth = projectGitUrl.replace("https://", f"https://{username}:{accessToken}@")
        helper.crateProject(ProjectGitUrlWithAuth, constants.CURRENT_PATH / rootGroupName, project["name"])


    while len(queue):
        group = queue[0]
        queue.pop(0)

        subGroups = helper.getSubGroups(str(group.id), accessToken, group.folderPath)
        queue = queue + subGroups

        projects = helper.getProjects(str(group.id), accessToken)

        for project in projects:
            projectGitUrl = project["http_url_to_repo"]
            ProjectGitUrlWithAuth = projectGitUrl.replace("https://", f"https://{username}:{accessToken}@")
            helper.crateProject(ProjectGitUrlWithAuth, group.folderPath, project["name"])
        
    print("all created done")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("")
        sys.exit(1)

    
    rootGroupId = sys.argv[1] 
    rootGroupName = sys.argv[2]
    username =  sys.argv[3]
    accessToken = sys.argv[4]

    os.makedirs(constants.CURRENT_PATH / rootGroupName, exist_ok=True)
    start(rootGroupId,rootGroupName,  username, accessToken)
    