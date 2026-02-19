import requests
import urllib.parse
import json


def check_proxynova(email):
    url = f"https://api.proxynova.com/comb?query={email}"
    headers = {'User-Agent': 'curl'}
    try:
        response = requests.get(url, headers=headers)
        return {'Proxynova': response.json()} 
    except Exception as e:
        print(e)
        return {'Proxynova': "No leaks"}


def check_xposedornot(email):
    try:
        encoded_email = urllib.parse.quote(email)
        url = f"https://api.xposedornot.com/v1/breach-analytics?email={encoded_email}"

        response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)

        if response.status_code != 200:
            print("Error XposedOrNot:", response.status_code)
            return {"XposedOrNot": "No leaks"}

        data = response.json()
        exposed = data.get("ExposedBreaches") or {}
        breaches = exposed.get("breaches_details", [])
        if len(breaches) == 0:
            return {"XposedOrNot": "No leaks"}

        return {"XposedOrNot": {"breaches": breaches, "total": len(breaches)}}

    except Exception as e:
        print(e)
        return {"XposedOrNot": "No leaks"}


def check_leaks(email):
    result = check_proxynova(email).copy() 
    result.update(check_xposedornot(email))
    return result

