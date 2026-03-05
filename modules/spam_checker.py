import requests


def check_spam(email):
	url = f"https://cleantalk.org/blacklists/{email}"

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
	}

	try:
		response = requests.get(url, headers=headers, timeout=10)
		response.raise_for_status()

		page = response.text.lower()

		if "spam activity not found" in page or "has no spam activity" in page:
			return {"spam": False, "site": url}

		return {"spam": True, "site": url}

	except requests.exceptions.Timeout:
		print("Error: timeout")
		return False

	except requests.exceptions.ConnectionError:
		print("Error: Connection error")
		return False

	except requests.exceptions.HTTPError as e:
		print(f"Error: http_error {e}")
		return False

	except Exception as e:
		print(f"Error: {e}")
		return False

