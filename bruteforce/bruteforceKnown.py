import os
import eth_utils
from web3 import Web3

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from dotenv import load_dotenv
load_dotenv(".env")

ALCHEMY_KEY_1 = os.environ.get("ALCHEMY_KEY_1")
ALCHEMY_KEY_2 = os.environ.get("ALCHEMY_KEY_2")

if not ALCHEMY_KEY_1 or not ALCHEMY_KEY_2:
    exit("Missing environnement variables in .env")

ETH_URL = "https://eth-mainnet.alchemyapi.io/v2/" + ALCHEMY_KEY_1
POL_URL = "https://polygon-mainnet.g.alchemy.com/v2/" + ALCHEMY_KEY_2
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[413,429,495,500,502,503,504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
web3_eth = Web3(Web3.HTTPProvider(ETH_URL, session = session))
web3_pol = Web3(Web3.HTTPProvider(POL_URL, session = session))



web3_eth.eth.account.enable_unaudited_hdwallet_features()

LG_DERIVATION = "M/44'/60'/0'/0"


with open("./wordlist.txt", "r") as file:
    words = file.readlines()

W1  = ['solve']
W2  = ['off']
W3  = ['spread']
W4  = ['foot']
W5  = ['leg']
W6  = ['arm']
W7  = ['music']
W8  = ['chat']
W9  = ['book']
W10 = ['cinnamon','gasp','infant','utility']
W11 = ['kiss']
W12 = ['follow']
W13 = ['wall']
W14 = ['cannon']
W15 = ['shop']
W16 = ['replace']
W17 = ['clean','grief']
W18 = ['choose','assault']
W19 = ['siren']
W20 = ['blind']
W21 = ['sentence']
W22 = ['slam']
W23 = ['glimpse']
W24 = ['weather']

WT = []
for i in range(2048):
    word = words[i].replace("\n","")
    WT += [word]

W17 = WT.copy()



nb_iter = len(W1)*len(W2)*len(W3)*len(W4)*len(W5)*len(W6)*len(W7)*len(W8)*len(W9)*len(W10)*len(W11)*len(W12)*len(W13)*len(W14)*len(W15)*len(W16)*len(W17)*len(W18)*len(W19)*len(W20)*len(W21)*len(W22)*len(W23)*len(W24)
with open("./logKW.txt", "a") as file:
    file.write(str(nb_iter)+"\n")

print(nb_iter)




compteur = 0

for w7 in W7:
    for w8 in W8:
        for w9 in W9:
            for w10 in W10:
                for w11 in W11:
                    for w12 in W12:
                        for w15 in W15:
                            for w16 in W16:
                                for w17 in W17:
                                    for w18 in W18:
                                        for w19 in W19:
                                            for w20 in W20:
                                                for w21 in W21:
                                                    for w22 in W22:
                                                        for w23 in W23:
                                                            for w24 in W24:

                                                                compteur += 1
                                                                seed = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(W1[0],W2[0],W3[0],W4[0],W5[0],W6[0],w7,w8,w9,w10,w11,w12,W13[0],W14[0],w15,w16,w17,w18,w19,w20,w21,w22,w23,w24)
                                                                try:
                                                                    lg_addr = web3_eth.eth.account.from_mnemonic(seed, account_path=LG_DERIVATION).address

                                                                    done = False
                                                                    while not done:
                                                                        try:
                                                                            eth_lg_balance = web3_eth.eth.get_balance(lg_addr) / (10**18)
                                                                            done = True
                                                                        except:
                                                                            pass
                                                                    
                                                                    if eth_lg_balance:
                                                                        with open("./logKW.txt", "a") as file:
                                                                            file.write(seed+"\n")
                                                                            file.write(str(lg_addr)+"\n")
                                                                        
                                                                except eth_utils.exceptions.ValidationError as err:
                                                                    pass

with open("./logKW.txt", "a") as file:
    file.write("\n"+str(compteur)+"\n")

print(compteur)