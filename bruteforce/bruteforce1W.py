import os
from bip_utils import Bip39MnemonicValidator
from web3 import Web3

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from dotenv import load_dotenv
load_dotenv(".env")

ALCHEMY_KEY_1 = os.environ.get("ALCHEMY_KEY_1")
ALCHEMY_KEY_2 = os.environ.get("ALCHEMY_KEY_2")
LOGFILE = "./log2W.txt"

if not ALCHEMY_KEY_1 or not ALCHEMY_KEY_2:
    exit("Missing environnement variables in .env")

ETH_URL = "https://eth-mainnet.g.alchemy.com/v2/"     + ALCHEMY_KEY_1
POL_URL = "https://polygon-mainnet.g.alchemy.com/v2/" + ALCHEMY_KEY_2
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[413,429,495,500,502,503,504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
web3_eth = Web3(Web3.HTTPProvider(ETH_URL, session = session))
web3_pol = Web3(Web3.HTTPProvider(POL_URL, session = session))



web3_eth.eth.account.enable_unaudited_hdwallet_features()

MM_DERIVATION = "m/44'/60'/0'/0/0"
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
W10 = ['cinnamon']
W11 = ['kiss']
W12 = ['follow']
W13 = ['wall']
W14 = ['cannon']
W15 = ['shop']
W16 = ['replace']
W17 = ['what']
W18 = ['chicken']
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


W = [W1, W2, W3, W4, W5, W6, W7, W8, W9, W10, W11, W12, W13, W14, W15, W16, W17, W18, W19, W20, W21, W22, W23, W24]

ALL = W.copy()



nb_iter = 0
not_sure = [10]
for i in not_sure:
    ALL = W.copy()
    ALL[i-1] = WT.copy()

    somme = 1
    for j in ALL:
        somme *= len(j)
    nb_iter += somme
    
with open("./log1W.txt", "a") as file:
    file.write(str(nb_iter)+"\n")
print(nb_iter)




compteur = 0
for i in not_sure:

    with open("./log1W.txt", "a") as file:
        file.write(str(i)+"\n")

    i -= 1
    ALL = W.copy()
    ALL[i] = WT.copy()

    for w7 in ALL[6]:
        for w8 in ALL[7]:
            for w9 in ALL[8]:
                for w10 in ALL[9]:
                    for w11 in ALL[10]:
                        for w12 in ALL[11]:
                            for w17 in ALL[16]:
                                for w18 in ALL[17]:
                                    for w19 in ALL[18]:
                                        for w20 in ALL[19]:
                                            for w21 in ALL[20]:
                                                for w22 in ALL[21]:
                                                    for w23 in ALL[22]:
                                                        for w24 in ALL[23]:
                                                            compteur += 1
                                                            seed = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(W1[0],W2[0],W3[0],W4[0],W5[0],W6[0],w7,w8,w9,w10,w11,w12,W13[0],W14[0],W15[0],W16[0],w17,w18,w19,w20,w21,w22,w23,w24)
                                                            if Bip39MnemonicValidator().IsValid(seed):
                                                                mm_addr = web3_eth.eth.account.from_mnemonic(seed, account_path=MM_DERIVATION).address
                                                                lg_addr = web3_eth.eth.account.from_mnemonic(seed, account_path=LG_DERIVATION).address
                                                                
                                                                eth_mm_nonce   = web3_eth.eth.get_transaction_count(mm_addr)
                                                                eth_mm_balance = web3_eth.eth.get_balance(mm_addr) / (10**18)
                                                                pol_mm_nonce   = web3_pol.eth.get_transaction_count(mm_addr)
                                                                pol_mm_balance = web3_pol.eth.get_balance(mm_addr) / (10**18)

                                                                eth_lg_nonce   = web3_eth.eth.get_transaction_count(lg_addr)
                                                                eth_lg_balance = web3_eth.eth.get_balance(lg_addr) / (10**18)
                                                                pol_lg_nonce   = web3_pol.eth.get_transaction_count(lg_addr)
                                                                pol_lg_balance = web3_pol.eth.get_balance(lg_addr) / (10**18)

                                                                if( eth_mm_nonce
                                                                    or eth_mm_balance
                                                                    or pol_mm_nonce
                                                                    or pol_mm_balance
                                                                    or eth_lg_nonce
                                                                    or eth_lg_balance
                                                                    or pol_lg_nonce
                                                                    or pol_lg_balance
                                                                ):
                                                                    with open("./log1W.txt", "a") as file:
                                                                        file.write("\n")
                                                                        file.write(seed)
                                                                        file.write("\n")
                                                                    print(seed)
                                                                    print("mm_addr: {}".format(mm_addr))
                                                                    print("lg_addr: {}".format(lg_addr))
                                                                    print("mm eth balance: {}".format(eth_mm_balance))
                                                                    print("lg eth balance: {}".format(eth_lg_balance))
                                                                    print("mm pol balance: {}".format(pol_mm_balance))
                                                                    print("lg pol balance: {}".format(pol_lg_balance))
                                                                    print("mm eth nonce:   {}".format(eth_mm_nonce))
                                                                    print("lg eth nonce:   {}".format(eth_lg_nonce))
                                                                    print("mm pol nonce:   {}".format(pol_mm_nonce))
                                                                    print("lg pol nonce:   {}".format(pol_lg_nonce))

print(compteur)