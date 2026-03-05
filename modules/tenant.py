import json
import requests


def is_domain_managed(email):
	try:
		url = f"https://login.microsoftonline.com/common/userrealm/{email}?api-version=2.1"
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.9",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"Content-Type": "application/json",
		}
		response = requests.get(url, headers=headers)

		data = response.json()
		result = data.get("NameSpaceType")

		if result == "Managed":
			return data
		else:
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



def check_tenant(email):
	try:
		if is_domain_managed(email):
			url = "https://login.microsoftonline.com/common/GetCredentialType"
			payload = {"username": email, "isOtherIdpSupported": True}

			headers = {
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				"Accept-Language": "en-US,en;q=0.9",
				"Connection": "keep-alive",
				"Upgrade-Insecure-Requests": "1",
				"Content-Type": "application/json",
			}

			response = requests.post(url, headers=headers, json=payload)
			
			if response.status_code != 200:
				print("Request failed:", response.status_code)
				return
			
			data = response.json()
			result = data.get("IfExistsResult")
			
			if result == 0:
				return {"Domain info": is_domain_managed(email), "Email info": response.json(), "Method": "MS-API"}
			elif result == 1:
				return {"Domain info": is_domain_managed(email), "Email info": f"{email} does NOT exist in tenant", "Method": "MS-API"}
			else:
				return {"Domain info": is_domain_managed(email), "Email info": f"{email} responded code {result} in tenant", "Method": "MS-API"}
		else:
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

