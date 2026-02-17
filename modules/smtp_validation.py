import smtplib
import dns.resolver
import json
import time
import random
import requests  


def check_smtp(target_email):
    domain = target_email.split('@')[-1]
    senders = ["info@gmail.com", "support@outlook.com", "noreply@yandex.ru"]
    sender_email = random.choice(senders)

    result = {
        "email": target_email,
        "method": "SMTP",
        "steps": [],
        "final_status": "unknown"
    }

    try:
        mx_records = [str(r.exchange).rstrip('.') for r in dns.resolver.resolve(domain, 'MX')]
        if not mx_records:
            return {"error": "No MX records found"}
        mx_host = mx_records[0]

        server = smtplib.SMTP(timeout=15)
        

        code, msg = server.connect(mx_host)
        result["steps"].append({"connect": {"code": code, "msg": msg.decode(errors='ignore')}})

        code, msg = server.helo("mail." + domain) 
        result["steps"].append({"helo": {"code": code, "msg": msg.decode(errors='ignore')}})

        code, msg = server.mail(sender_email)
        result["steps"].append({"mail_from": {"sender": sender_email, "code": code, "msg": msg.decode(errors='ignore')}})

        if code != 250:
            result["final_status"] = "blocked_at_mail_from"
        else:
            time.sleep(1) 
            code, msg = server.rcpt(target_email)
            result["steps"].append({"rcpt_to": {"code": code, "msg": msg.decode(errors='ignore')}})
            result["final_status"] = "valid" if code == 250 else "invalid"

        server.quit()
    except Exception as e:
        result["final_status"] = f"failed: {str(e)[:50]}"

    return result

