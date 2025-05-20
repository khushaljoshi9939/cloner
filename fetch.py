import requests

# get the json data for subgroups and projects
def getGitLabData(url, token):
    try:
        headers = {
            'PRIVATE-TOKEN': token,
            'User-Agent': 'MyApp/1.0',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)  
        response.raise_for_status()
        return { "success": True, "data": response.json() }
    except :
        return { "success": False }
