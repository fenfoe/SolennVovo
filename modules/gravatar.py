import json
import requests
from hashlib import md5


def check_gravatar(email):
	email_hash = md5(email.strip().lower().encode()).hexdigest()
	url = f"https://en.gravatar.com/{email_hash}.json"
	try:
		headers = {
			"User-Agent":
				"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
			"Accept-Language": "en-US,en;q=0.9",
			"Referer": "https://www.google.com",
			"Origin": "https://www.google.com"
		}
		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			data = response.json()
			if 'entry' in data:
				entry = data['entry'][0]
				return entry
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

