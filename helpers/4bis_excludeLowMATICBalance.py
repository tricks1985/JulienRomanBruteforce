import os, json
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
web3_pol = Web3(Web3.HTTPProvider(ETH_URL, session = session))

# MATIC contract addr on Ethereum
MATIC_ADDR = "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0"

with open('3_noETHBalance.txt') as file:
    addrs = file.readlines()

with open("maticABI.txt", "r") as file:
    maticABI = json.load(file)

maticSC = web3_pol.eth.contract(address=MATIC_ADDR, abi=maticABI)


# get addrs with MATIC balance greater than 10 on Ethereum
for addr in addrs:
    addr = addr.replace("\n","")

    polBalance = maticSC.functions.balanceOf(addr).call()
    polBalance = Web3.fromWei(polBalance, 'ether')

    if polBalance >= 10:
        with open("./4bis_noMATICBalance.txt", "a") as file:
            file.write(addr+"\n")
