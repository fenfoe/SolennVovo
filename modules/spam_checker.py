import requests


def check_spam(email):
    try:
        url = f"https://cleantalk.org/blacklists/{email}"
        page = requests.get(url).text
        if 'spam activity not found' in page:
            return {'spam': False, 'site': f"https://cleantalk.org/blacklists/{email}"}
        elif 'Reached maximum queries rate to blacklists' in page:
            return False
        else:
            return {'spam': True, 'site': f"https://cleantalk.org/blacklists/{email}"}
    except Exception as e:
        print(e)

