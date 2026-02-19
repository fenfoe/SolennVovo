import json
import requests


def is_domain_managed(email):
    try:
	    url = f"https://login.microsoftonline.com/common/userrealm/{email}?api-version=2.1"
	    headers = {"Content-Type": "application/json"}
	    response = requests.get(url, headers=headers)

	    data = response.json()
	    result = data.get("NameSpaceType")

	    if result == "Managed":
		    return data
	    else:
		    return False
    except Exception as e:
        print(e)
        return False


def check_tenant(email):
    try:
	    if is_domain_managed(email):
		    url = "https://login.microsoftonline.com/common/GetCredentialType"
		    payload = {"username": email, "isOtherIdpSupported": True}
		    headers = {"Content-Type": "application/json"}
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
    except Exception as e:
        print(e)
        return False

