import streamlit as st
import json
import base64
import requests

# 🌍 Global array to store no entry zone shapes
shapes = []

# ***********************************************************************
# * Utility functions for handling GitHub storage
# ***********************************************************************

# List of files in area/ folder from GitHub API
def get_area_files(path):
    token = st.secrets["github_token"]
    owner = st.secrets["repo_owner"]
    repo = st.secrets["repo_name"]
   
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(api_url, headers={"Authorization": f"token {token}"})
    #response = requests.get(api_url)
    if response.status_code != 200:
        st.error("Failed to fetch area files from GitHub.")
        return []
    files = response.json()
    return [f["name"] for f in files if f["name"].endswith(".json") and f["name"] != "blankarea.json"]

# Load a JSON file from GitHub and count zones
def load_area_file(path, file_name):
    owner = st.secrets["repo_owner"]
    repo = st.secrets["repo_name"]
    raw_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}/"+ file_name
    response = requests.get(raw_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        zones = data.get("zones", [])
        return zones
    return []

# Save JSON file to GitHub
def save_to_github(path, content_str, commit_message):
    token = st.secrets["github_token"]
    owner = st.secrets["repo_owner"]
    repo = st.secrets["repo_name"]
    branch = st.secrets["branch"]

    # GitHub API URL for the file
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    # Get the SHA if the file already exists (required for updating)
    sha = None
    get_response = requests.get(api_url, headers={"Authorization": f"token {token}"})
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
    response = requests.put(api_url, headers={"Authorization": f"token {token}"}, json=data)
    return response

# ***********************************************************************
# * END OF Utility functions for handling GITHUB storage 
# ***********************************************************************