import re
import shutil
import subprocess


def run_if_installed(app_name, args=None):
    path = shutil.which(app_name)
    if path is None:
        return False

    command = [path] + (args or [])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


def extract_sites(output_text):
    sites = []
    for line in output_text.splitlines():
        if line.startswith("[+] ") and "," not in line:
            sites.append(line[4:].strip())
    return sites


def check_holehe(email):
    output = run_if_installed(
        "holehe",
        [email, "--only-used"]
    )
    
    if output:
        sites = extract_sites(output)
        if sites == []:
            return False
        return {"sites": sites}
    else:
        print("Install holehe to use this checker\nVisit https://github.com/megadose/holehe")
        return False
