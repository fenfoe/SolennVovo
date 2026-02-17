import json
import requests


def check_github(email):
    url = f"https://api.github.com/search/commits?q=author-email:{email}"
    headers = {"Accept": "application/vnd.github.cloak-preview"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get('items', [])
            if items:
                author = items[0]['commit']['author']
                user_profile = items[0]['author']
                return {"Author": author, "User profile": user_profile}
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

