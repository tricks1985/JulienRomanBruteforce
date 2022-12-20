import os
from web3 import Web3

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from dotenv import load_dotenv
load_dotenv(".env")

ALCHEMY_KEY = os.environ.get("ALCHEMY_KEY")

if not ALCHEMY_KEY:
    exit("Missing environnement variables in .env")

# check on Polygon network and not ethereum
POL_URL = "https://polygon-mainnet.g.alchemy.com/v2/" + ALCHEMY_KEY

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[413,429,495,500,502,503,504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
web3_pol = Web3(Web3.HTTPProvider(POL_URL, session = session))


with open('3_noETHBalance.txt') as file:
    addrs = file.readlines()


# get addrs with MATIC balance greater than 10 on Polygon
for addr in addrs:
    addr = addr.replace("\n","")

    polBalance = web3_pol.eth.get_balance(addr)
    polBalance = Web3.fromWei(polBalance, 'ether')

    if polBalance >= 10:
        with open("./4_noMATICBalance.txt", "a") as file:
            file.write(addr+"\n")
