import requests


def check_hudsonrock(email):
	hudson_rock_url = (
			"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
			f"search-by-email?email={requests.utils.quote(email)}"
		)
	try:
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.9",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
		}
		response = requests.get(hudson_rock_url, headers=headers, timeout=10)
		data = response.json()
		if data.get("stealers") and len(data["stealers"]) > 0:
			del data[next(iter(data))]
			return data
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

