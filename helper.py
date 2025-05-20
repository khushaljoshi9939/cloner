from fetch import getGitLabData
from subGroups import SubGroup
import constants
import subprocess
import os

# get sub groups id
def getSubGroups(groupId, token, parentPath):
    url = constants.GITLAB_BASE_API + "/" + groupId + "/subgroups"
    response = getGitLabData(url, token)

    if not response["success"]:
        raise Exception("gitlab id or token is not correct")
    
    filteredGroups = []

    for subGroup in response["data"]:
        filteredGroups.append(SubGroup(subGroup["id"], subGroup["name"], parentPath / subGroup["name"]))

    return filteredGroups

# get projects from  id
def getProjects(groupId, token):
    url = constants.GITLAB_BASE_API + "/" + groupId + "/projects"
    response = getGitLabData(url, token)

    if not response["success"]:
        raise Exception("gitlab id or token is not correct")
    
    return response["data"]

#crate projects
def crateProject(cloneUrl, cloneDirPath, projectName):
    projectFolderDir = cloneDirPath / projectName
    if os.path.exists(projectFolderDir):
        print(f"[SKIP] {cloneUrl} already exists.")
        return
    
    print(f"[CLONING] {cloneUrl}")
    subprocess.run(["git", "clone", cloneUrl, projectFolderDir], check=True)