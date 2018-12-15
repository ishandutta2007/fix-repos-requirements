import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, timedelta
import subprocess
from requests import session

import pprint as pp
import base64
import argparse
import constants
import json

headers = {'Authorization': 'token %s' % constants.GITHUB_API_TOKEN}

def try_variants(url):
	for variant in ['README', 'README.txt', 'Readme.md','readme.md', 'readme.MD', 'README.MD', 'README.rst', 'Readme.rst', 'readme.rst', 'README.mdown', 'ReadMe.md']:
		time.sleep(1)
		r = requests.get(url.replace('README.md', variant), headers=headers)
		repo_item = json.loads(r.text or r.content)
		try:
			if repo_item['message']=='Not Found':
				print(url.replace('README.md', variant), repo_item['message'])
				continue
			return repo_item, variant
		except Exception as e:
			print(e)
			return repo_item, variant
	return repo_item, None

def clone(url):
	time.sleep(2)
	subprocess.call(["git", "clone", url, "mypyrepos/"+url.split('/')[-1]])

def is_python_repo(url):
	PATH = "mypyrepos/"+url.split('/')[-1]
	for _, _, filenames in os.walk(PATH):
		for f in filenames:
			if os.path.splitext(f)[1] == '.py':
				return True
	return os.path.exists(PATH+ "/requirements.txt")

def revert(url):
	with open('revert_cmds.sh', 'a') as f:
		f.write("cd $(echo $PWD'/mypyrepos/" + url.split('/')[-1] + "')\n")
		f.write("git status\n")
		f.write("git checkout requirements.txt\n")
		f.write("git status\n")
		f.write("echo '===" + url.split('/')[-1] + " reverted==='\n")
		f.write("cd ../..\n")

def fix(url):
	with open('fix_cmds.sh', 'a') as f:
		f.write("cd $(echo $PWD'/mypyrepos/" + url.split('/')[-1] + "')\n")
		f.write("git status\n")
		f.write("pip install -r requirements.txt\n")
		f.write("git status\n")
		f.write("pip install pigar\n")
		f.write("pigar\n")
		f.write("git status\n")
		f.write("git add requirements.txt\n")
		f.write("git status\n")
		f.write("echo '===" + url.split('/')[-1] + " done==='\n")
		f.write("cd ../..\n")

def delete_clones(url):
	with open('delete_clones_cmds.sh', 'a') as f:
		f.write("rm -rf $(echo $PWD'/mypyrepos/" + url.split('/')[-1] + "')\n")

def commit_push(url):
	with open('commit_push_cmds.sh', 'a') as f:
		f.write("cd $(echo $PWD'/mypyrepos/" + url.split('/')[-1] + "')\n")
		f.write("git status\n")
		f.write("git commit -m \"fixing requirements.txt\"\n")
		f.write("git status\n")
		f.write("git push\n")
		f.write("git status\n")
		f.write("echo '===" + url.split('/')[-1] + " done==='\n")
		f.write("cd ../..\n")

def delete_shell_scripts():
	for f in os.listdir('.'):
		if os.path.splitext(f)[1] == '.sh':
			os.unlink(f)

def main():
	delete_shell_scripts()
	with open('clone_url-list.csv','r') as fp:
		url = fp.readline().strip()
		cnt = 1
		while url:
			print("Repo {}: {}".format(cnt, url.strip()))
			clone(url)
			print(url, is_python_repo(url))
			if is_python_repo(url):
				revert(url)
				fix(url)
				commit_push(url)
			delete_clones(url)
			cnt += 1
			url = fp.readline().strip()

if __name__ == '__main__':
	main()
