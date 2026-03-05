import json
import requests


def check_github(email):
	url = f"https://api.github.com/search/commits?q=author-email:{email}"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
	}
	
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			items = response.json().get('items', [])
			if items:
				author = items[0]['commit']['author']
				user_profile = items[0]['author']
				return {"Author": author, "User profile": user_profile}
		return False
	except requests.exceptions.Timeout:
		print("Error: timeout")
		return False

	except requests.exceptions.ConnectionError:
		print("Error: Connection error")
		return False

	except requests.exceptions.HTTPError as e:
		print(f"Error: http_error: {e}")
		return False

	except Exception as e:
		print(f"Error: {e}")
		return False

