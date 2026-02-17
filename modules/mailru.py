import requests


def check_mailru(email):
    headers = {
        'authority': 'account.mail.ru',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://account.mail.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://account.mail.ru/recovery?email={email}',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'accept-language': 'ru',
    }

    if email.split('@')[1] not in ["mail.ru", "bk.ru", "inbox.ru", "list.ru", "internet.ru"] :
        return False

    data = f'email={email}&htmlencoded=false'.replace('@', '%40')
    res = requests.post('https://account.mail.ru/api/v1/user/password/restore', headers=headers, data=data)

    if res.json()["status"] == 200:
        return res.json()["body"]
    return False

