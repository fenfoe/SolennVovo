from create_html import list_to_html, dict_to_table, generate_html
from modules.duolingo import check_duolingo
from modules.flickr_osint.flickr import check_flickr
from modules.github import check_github
from modules.gravatar import check_gravatar
from modules.holehe_using import check_holehe
from modules.hudsonrock import check_hudsonrock
from modules.leaked_passwords import check_leaks
from modules.mailru import check_mailru
from modules.ok import check_OK
from modules.proton import check_proton
from modules.smtp_validation import check_smtp
from modules.spam_checker import check_spam
from modules.tenant import check_tenant
from modules.trello_osint.trello import check_trello

import argparse
import json
import os


CHECKERS = {
	"spam": check_spam,
	"smtp": check_smtp,
	"duolingo": check_duolingo,
	"gravatar": check_gravatar,
	"holehe": check_holehe,
	"mailru": check_mailru,
	"ok": check_OK,
	"github": check_github,
	"proton": check_proton,
	"leaks": check_leaks,
	"tenant": check_tenant,
	"hudsonrock": check_hudsonrock,
	"trello": check_trello,
	"flickr": check_flickr
}


def run_checks(email: str, selected=None, output="terminal"):
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

	if output == "terminal":
		print("\nResults:\n")
		print(json.dumps(results, indent=4))

	elif output == "json":
		filename = f"results/{email}_results.json"
		with open(filename, "w") as f:
			json.dump(results, f, indent=4)

		print(f"\nJSON saved to {filename}")

	elif output == "html":
		generate_html(email, results)


def list_checkers(parser):
	print("Available checkers:\n")

	for i, name in enumerate(CHECKERS.keys(), 1):
		print(f"{i}. {name}")

	print(f"\nNumber of checkers: {len(CHECKERS)}")
	parser.exit()


def main():
	parser = argparse.ArgumentParser(description="Email Intelligence Checker")

	parser.add_argument("--email", type=str, help="Target email address")
	parser.add_argument("--only", nargs="+", help="Run only specific checks (e.g. --only spam duolingo)")
	parser.add_argument("--output", choices=["terminal", "json", "html"], default="html", help="Output format: terminal, json, or html")
	parser.add_argument("--list-checkers", action="store_true", help="Show all available checker names and exit")

	args = parser.parse_args()

	if args.list_checkers:
		list_checkers(parser)

	if not args.email:
		parser.error("--email is required unless using --list-checkers")

	run_checks(args.email, args.only, args.output)


if __name__ == "__main__":
	main()

