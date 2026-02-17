import argparse
import requests
from bs4 import BeautifulSoup


OK_LOGIN_URL = \
    'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
OK_RECOVER_URL = \
    'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'


def check_OK(login_data):
    session = requests.Session()
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
    session.get(f'{OK_LOGIN_URL}&st.email={login_data}', headers=user_agent)
    request = session.get(OK_RECOVER_URL)
    root_soup = BeautifulSoup(request.content, 'html.parser')
    soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
    if soup:
        account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
        masked_email = soup.find('button', {'data-l': 't,email'})
        masked_phone = soup.find('button', {'data-l': 't,phone'})
        if masked_phone:
            masked_phone = masked_phone.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if masked_email:
            masked_email = masked_email.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if account_info:
            masked_name = account_info.find('div', {'class': 'ext-registration_username_header'})
            if masked_name:
                masked_name = masked_name.get_text()
            account_info = account_info.findAll('div', {'class': 'lstp-t'})
            if account_info:
                profile_info = account_info[0].get_text()
                profile_registred = account_info[1].get_text()
            else:
                profile_info = None
                profile_registred = None
        else:
            return None

        result = (f"[+] Odnoklassniki Account Found\n├masked_name: {masked_name}\n├masked_email: {masked_email}\n├masked_phone: {masked_phone}"
                  f"\n├profile_info: {profile_info}\n└profile_registred: {profile_registred}\n\n")
        print(result)
        return {"Masked name": masked_name, "Masked email":masked_email, "Masked phone":masked_phone, "Profile info":profile_info,"Profile registred":profile_registred}
    if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
        return False

