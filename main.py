import argparse
import os
from create_html import list_to_html, dict_to_table, generate_html
from modules.duolingo import check_duolingo
from modules.github import check_github
from modules.gravatar import check_gravatar
from modules.holehe_using import check_holehe
from modules.leaked_passwords import check_leaks
from modules.mailru import check_mailru
from modules.ok import check_OK
from modules.proton import check_proton
from modules.smtp_validation import check_smtp
from modules.spam_checker import check_spam
from modules.tenant import check_tenant


CHECKERS = {
    "spam": check_spam,
    "leaks": check_leaks,
    "duolingo": check_duolingo,
    "gravatar": check_gravatar,
    "holehe": check_holehe,
    "mailru": check_mailru,
    "ok": check_OK,
    "github": check_github,
    "proton": check_proton,
    "smtp": check_smtp,
    "tenant": check_tenant
}


def run_checks(email: str, selected=None):
    selected = selected or CHECKERS.keys()

    results = {}

    for name in selected:
        checker = CHECKERS.get(name)
        if not checker:
            continue

        print(f"▶ Running {name} check...")

        try:
            result = checker(email)


            if isinstance(result, dict):
                results[name] = result

        except Exception as e:
            print(f"Error in {name}: {e}")

    generate_html(email, results)


def list_checkers(parser):
    print("Available checkers:")
    print("\n".join(CHECKERS.keys()))
    parser.exit()


def main():
    parser = argparse.ArgumentParser(description="Email Intelligence Checker")

    parser.add_argument("--email", type=str, help="Target email address")
    parser.add_argument("--only", nargs="+", help="Run only specific checks (e.g. --only spam duolingo)")
    parser.add_argument("--list-checkers", action="store_true", help="Show all available checker names and exit")

    args = parser.parse_args()

    if args.list_checkers:
        list_checkers(parser)

    if not args.email:
        parser.error("--email is required unless using --list-checkers")

    run_checks(args.email, args.only)


if __name__ == "__main__":
    main()

