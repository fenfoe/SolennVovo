import json
import pgpy
import requests
from datetime import datetime


def check_proton(email):
    url = f"https://api.protonmail.ch/pks/lookup?op=get&search={email}"
    try:
        protonLst = ["protonmail.com", "protonmail.ch", "pm.me", "proton.me"]
        if email.split('@')[1] not in protonLst:
            return False

        response = requests.get(url, timeout=10)
        if response.status_code != 200 or "-----BEGIN PGP PUBLIC KEY BLOCK-----" not in response.text:
            return False

        key_block = response.text
        key, _ = pgpy.PGPKey.from_blob(key_block)
        
        creation_time = key.created
        data = {"Key Created":f"{creation_time.strftime('%Y-%m-%d %H:%M:%S')} UTC", "Fingerprint":f"{key.fingerprint}"}
        return data

    except Exception as e:
        print(f"[-] Error: {e}")
        return False 

