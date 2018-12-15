# reach-github-issuers

This is a repo which bulk update requirements.txt of all of my python repos with packages only found in code.

### To run:

1. `python3 github-nonforked-repo-lister.py` will create all csv owned by me in `url-list.csv` file

2. `python3 github-repo-cloner.py`will update README.md of each of them

3. `bash fix_cmds.sh`

4. Review projects under mypyrepos/{reponame}. In case something undesirable happens you can use `bash review_cmds.sh`

5. If all is good to commit and push run `bash commit_push_cmds.sh`

### Support:

If you want the good work to continue please support us on

* [PAYPAL](https://www.paypal.me/ishandutta2007)
* [BITCOIN ADDRESS: 3LZazKXG18Hxa3LLNAeKYZNtLzCxpv1LyD](https://www.coinbase.com/join/5a8e4a045b02c403bc3a9c0c)
