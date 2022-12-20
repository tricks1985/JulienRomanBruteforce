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

ETH_URL = "https://eth-mainnet.alchemyapi.io/v2/" + ALCHEMY_KEY
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[413,429,495,500,502,503,504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
web3_eth = Web3(Web3.HTTPProvider(ETH_URL, session = session))


with open('1_theGraphAddr.txt') as file:
    addrs = file.readlines()


# exclude contracts
for addr in addrs:
    addr = Web3.toChecksumAddress(addr.replace("\n",""))

    if not web3_eth.eth.get_code(addr) :
        with open("2bis_noContracts.txt", "a") as file:
            file.write(addr+"\n")
