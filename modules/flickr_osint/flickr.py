import requests
import time
from urllib.parse import quote

base_url = "https://www.flickr.com/services/rest"
api_key = "Enter your API-key"


def check_flickr(email):
	try:
		params = {
			"format": "json",
			"nojsoncallback": 1,  
			"api_key": api_key,
			"method": "flickr.people.search",
			"username": email,   
			"cachebust": int(time.time() * 1000)
		}
		
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.9",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
		}

		response = requests.get(base_url, params=params)
		data = response.json()

		if data['people']['count'] == 0:
			return False
		elif data['people']['count'] == 1:
			data['people']['person'][0]['profile'] = "https://www.flickr.com/photos/" + data['people']['person'][0]['nsid']
			return {"Account": data['people']['person'][0]}
		else:
			return {"Account": data['people']['person']}

	except requests.exceptions.Timeout:
		print("Error: timeout")
		return False

	except requests.exceptions.ConnectionError:
		print("Error: Connection error")
		return False

	except requests.exceptions.HTTPError as e:
		print(f"Error: http_error {e}")
		return False

	except:
		print("Error: unable to use this checker")
		print("Maybe, you have to update your api_key\n Visit: https://www.flickr.com/")
		return False
