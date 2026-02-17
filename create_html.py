import os


ICON_MAP = {
    "spam": "🚫",
    "leaks": "💦",
    "duolingo": "🦉",
    "gravatar": "🟦",
    "mailru": "🚙",
    "ok": "📙",
    "github": "🐙",
    "proton": "📧",
    "smtp": "📫",
    "tenant": "🛬",
    "holehe": "🌏"
}


DESCRIPTION_MAP = {
    "spam": "Email spam, also referred to as junk email, spam mail, or simply spam, refers to unsolicited messages sent in bulk via email.",
    "leaks": "This tool allows you to find if an email address was leaked in data breaches.\n But for more information visit: https://haveibeenpwned.com/",
    "duolingo": "Duolingo, Inc. is an American educational technology company that produces learning apps and provides language certification.",
    "gravatar": "Gravatar is a service for providing globally unique avatars and was created by Tom Preston-Werner. Since 2007, it has been owned by Automattic, having integrated it into their WordPress.com blogging platform.",
    "mailru": "Mail.ru is one of the most popular email services in Russia and Eastern Europe, with over 100 million active users.",
    "ok": "Odnoklassniki, abbreviated as OK or OK.ru, is a social networking service and online video sharing website primarily in Russia and former Soviet Republics.",
    "github": "GitHub is a proprietary developer platform that allows developers to create, store, manage, and share their code.",
    "proton": "Proton Mail is a Swiss end-to-end encrypted email service launched in 2014.",
    "smtp": "The Simple Mail Transfer Protocol is an Internet standard communication protocol for electronic mail transmission.",
    "tenant": "A Microsoft tenant is a dedicated instance of Microsoft 365 services that stores an organization's data in a specific location, such as Europe or North America. It is created when someone purchases Microsoft products and is used for managing user accounts, applications, and resources within your organization.",
    "holehe": "Holehe checks if an email is attached to an account on sites like twitter, instagram, imgur and more than 120 others."
}


def list_to_html(items):
    html = "<ul>"
    for item in items:
        if isinstance(item, dict):
            html += "<li>" + dict_to_table(item) + "</li>"
        else:
            html += f"<li>{item}</li>"
    html += "</ul>"
    return html


def dict_to_table(data: dict):
    html = "<table border='1' cellpadding='6' cellspacing='0'>"

    for key, value in data.items():
        html += "<tr>"
        html += f"<td class='key'><strong>{key}</strong></td>"
        html += "<td>"

        if isinstance(value, dict):
            html += dict_to_table(value)  # recursion
        elif isinstance(value, list):
            html += list_to_html(value)
        else:
            html += str(value)

        html += "</td></tr>"

    html += "</table>"
    return html


def generate_html(email: str, results: dict):
    os.makedirs("results", exist_ok=True)

    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" /><title>EmailSearch</title>
<style>
body {background-color: #f2f2f2;}
.content {display: flex; flex-wrap: wrap;}
.block {width: 45%; margin: 1%; border-radius: 10px; padding: 10px; background-color: white;}
.left {width: 80%; margin-left: 20%;}
.right {width: 20%; position: fixed; right: 0; top: 80px;}
.title {font-size: 24px; font-weight: bold; margin-top: 20px;}
.block-title {font-size: 18px; font-weight: bold;}
.block-text {font-size: 14px; margin-top: 5px; line-height: 1.5em;}
.block-text p {margin: 5px 0;}
.nav {background-color: #333; position: fixed; left: 0; top: 0; width: 15%; height: 100%; overflow: auto;}
.nav a {color: white; display: block; padding: 10px; text-decoration: none;}
.nav a:hover {background-color: #ddd; color: black;}
.active {background-color: #4CAF50;}
.nav-title {color: white; font-size: 24px; font-weight: bold; padding: 10px;}
.block-description {
    font-size: 14px;
    color: #555;
    margin: 6px 0 10px 0;
}
</style>
</head>
<body>
        <div class='nav'>
            <div class='nav-title'>Table of Contents</div>
    """

    for i, name in enumerate(results.keys(), 1):
        icon = ICON_MAP.get(name, "📁")
        html += f"<a href='#p{i}'><b>{icon} {name}</b></a>"

    html += "</div><div class='left'><div class='content'>"

    for i, (name, data) in enumerate(results.items(), 1):
        icon = ICON_MAP.get(name, "📁")
        description = DESCRIPTION_MAP.get(name, "📁")
        html += f"""
        <div id='p{i}' class='block'>
            <div class='block-title'><b>{icon} {name}</b></div>
            <div class='block-description'>{description}</div>
            <div class='block-text'>{dict_to_table(data)}</div>
        </div>
        """

    html += f"""
        </div>
    <div class='right'>
    </div>
    </body>
    </html>
    """

    with open(f"results/{email}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ HTML report saved to results/{email}.html")
