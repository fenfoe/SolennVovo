import requests
import json


def check_leaks_proxynova(email):
    url = f"https://api.proxynova.com/comb?query={email}"
    headers = {'User-Agent': 'curl'}
    try:
        response = requests.get(url, headers=headers)
        return response.json() 
    except Exception as e:
        print(e)

