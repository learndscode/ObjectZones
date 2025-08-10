import json
import base64
import requests

def upload_to_github(token, owner, repo, branch, path, content_str, commit_message):
    # GitHub API URL for the file
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    # Get the SHA if the file already exists (required for updating)
    sha = None
    get_response = requests.get(url, headers={"Authorization": f"token {token}"})
    if get_response.status_code == 200:
        sha = get_response.json()["sha"]
    
    # Encode file content to Base64
    encoded_content = base64.b64encode(content_str.encode()).decode()
    
    data = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch
    }
    if sha:
        data["sha"] = sha  # required to overwrite

    # Upload file
    response = requests.put(url, headers={"Authorization": f"token {token}"}, json=data)
    return response