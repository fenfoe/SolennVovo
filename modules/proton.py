import json
import pgpy
import requests
from datetime import datetime


def check_proton(email):
	url = f"https://api.protonmail.ch/pks/lookup?op=get&search={email}"
	try:
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.9",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
		} 

		protonLst = ["protonmail.com", "protonmail.ch", "pm.me", "proton.me"]
		if email.split('@')[1] not in protonLst:
			return False

		response = requests.get(url, headers=headers, timeout=10)
		if response.status_code != 200 or "-----BEGIN PGP PUBLIC KEY BLOCK-----" not in response.text:
			return False

		key_block = response.text
		key, _ = pgpy.PGPKey.from_blob(key_block)
		
		creation_time = key.created
		data = {"Key Created":f"{creation_time.strftime('%Y-%m-%d %H:%M:%S')} UTC", "Fingerprint":f"{key.fingerprint}"}
		return data

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

