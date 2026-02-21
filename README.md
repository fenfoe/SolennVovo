# Solenn Vovo
Solenn Vovo - OSINT program written in Python3 that searches for information about email addresses from various sources

## Features
- You can select a separate module(s) for searching
- Output to HTML file
- No API-keys (maybe later)
- Easy to install and to use

## Installation
```bash
git clone https://github.com/fenfoe/SolennVovo.git
cd SolennVovo
pip3 install requests holehe PGPy
```
## Usage 
```bash
python3 main.py -h
python3 main.py --email <target>  # To run all checkers
python3 main.py --email <target> --only duolingo gravatar  # To run only duolingo and gravatar checkers
python3 main.py --list-checkers   # To list all available checkers
```
![Run](images/run.png)

## Output example
![Result 1](images/res1.png)
![Result 2](images/res2.png)

## Disclaimer
This tool is for educational purposes only. Use of this tool is at your own risk. The author is not responsible for any outcomes resulting from its use.
