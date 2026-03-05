import requests
import json
import os
import random
import time
import re
from urllib.parse import quote


id_board = "Enter your ID board"
id_organization = "Enter your ID organization"


def extract_id_member(cookies):
	for cookie in cookies:
		if cookie.get('name') == 'idMember':
			return cookie.get('value')
	return None


def check_trello(email):
	try:
		with open("modules/trello_osint/trello_cookies.json") as file:
			cookies = json.load(file)
	except Exception as e:
		print("Did you forget to write your cookies in a json file?")
		print(e)
		return False

	# Extract idMember for reqid
	id_member = extract_id_member(cookies)
	# Loosen domain check to ensure we catch .trello.com, trello.com, etc.
	final_cookies = [c for c in cookies if 'trello.com' in c.get('domain', '')]
	cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in final_cookies])
	
	# Default reqid if idMember missing (unlikely if cookies valid)
	req_id_prefix = id_member if id_member else "unknown"

	headers = {
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'accept-language': 'es,en;q=0.9,es-419;q=0.8',
		'priority': 'u=1, i',
		'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'x-requested-with': 'XMLHttpRequest',
		'x-trello-client-version': 'build-230472',
		'x-trello-reqid': f"{req_id_prefix}-{random.random()}",
		'cookie': cookie_string,
		'referer': 'https://trello.com/b/pllfr53F/mi-tablero-de-trello',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
	}
	
	search_url = f"https://trello.com/1/search/members/?idBoard={id_board}&idOrganization={id_organization}&idEnterprise=&query={quote(email)}"
	
	try:
		response = requests.get(search_url, headers=headers)
		if response.status_code != 200:
			return False
		data = response.json()
		if not isinstance(data, list) or len(data) == 0:
			return False
			
		user = data[0]
		if user.get('memberType') == 'ghost':
			return False
		
		# Avatar
		avatar_hash = user.get('avatarHash')
		avatar_url = user.get('avatarUrl')
		
		# Helper to ensure avatar URL is correct
		if avatar_url:
			 # Trello Internal API returns avatarUrl without extension (e.g. .../hash)
			 # We need to append /original.png
			 if not avatar_url.endswith('.png') and not avatar_url.endswith('.jpg'):
				 user["avatarUrl"] = f"{avatar_url}/original.png"

			 if any(size in avatar_url for size in ["/170.png", "/30.png"]):
				 user["avatarUrl"] = avatar_url.replace("/170.png", "/original.png").replace( "/30.png", "/original.png")

		# If still no avatar_url but we have hash
		if not avatar_url and avatar_hash:
			 user["avatarUrl"] = f"https://trello-members.s3.amazonaws.com/{user['id']}/{avatar_hash}/original.png"
		
		return {"User Profile": user}
	except Exception as e:
		print(e)
		return False
