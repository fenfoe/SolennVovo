import requests
import urllib.parse
import json


def check_proxynova(email):
	url = f"https://api.proxynova.com/comb?query={email}"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "curl",
	}

	try:
		response = requests.get(url, headers=headers)
		return {'Proxynova': response.json()} 

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


def check_xposedornot(email):
	try:
		encoded_email = urllib.parse.quote(email)
		url = f"https://api.xposedornot.com/v1/breach-analytics?email={encoded_email}"
		headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
		"Accept": "application/json",
		}		

		response = requests.get(url, headers=headers, timeout=10)

		if response.status_code != 200:
			print("Error XposedOrNot:", response.status_code)
			return {"XposedOrNot": "No leaks"}

		data = response.json()
		exposed = data.get("ExposedBreaches") or {}
		breaches = exposed.get("breaches_details", [])
		if len(breaches) == 0:
			return {"XposedOrNot": "No leaks"}

		return {"XposedOrNot": {"breaches": breaches, "total": len(breaches)}}

	except requests.exceptions.Timeout:
		print("Error: timeout")
		return {"XposedOrNot": "No leaks"}

	except requests.exceptions.ConnectionError:
		print("Error: Connection error")
		return {"XposedOrNot": "No leaks"}

	except requests.exceptions.HTTPError as e:
		print(f"Error: http_error: {e}")
		return {"XposedOrNot": "No leaks"}

	except Exception as e:
		print(f"Error: {e}")
		return {"XposedOrNot": "No leaks"}

	except Exception as e:
		print(e)
		return {"XposedOrNot": "No leaks"}


def check_leaks(email):
	result = check_proxynova(email).copy() 
	result.update(check_xposedornot(email))
	return result

