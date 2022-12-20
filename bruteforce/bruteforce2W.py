import os
import eth_utils
from datetime import datetime
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


with open("../wordlist.txt", "r") as file:
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
W17 = ['what']
W18 = ['depend']
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


start = datetime.now()

nb_iter = 0
not_sure = [17,18]


theoriq_compt = (len(not_sure) * (len(not_sure)-1) / 2) *len(WT)*len(WT)
with open(LOGFILE, "a") as file:
    file.write("Start time: " + str(start) + '\n')
    file.write("Calcul theorique: " + str(theoriq_compt)+"\n")

compteur = 0
for i in range(len(not_sure)):

    ALL = W.copy()
    ALL[not_sure[i]-1] = WT.copy()

    for j in range(i+1, len(not_sure)):

        with open(LOGFILE, "a") as file:
            file.write(str(not_sure[i])+" "+str(not_sure[j])+"\n")

        ALLT = ALL.copy()
        ALLT[not_sure[j]-1] = WT.copy()


        for w8 in ALLT[7]:
            for w10 in ALLT[9]:
                for w11 in ALLT[10]:
                    for w17 in ALLT[16]:
                        for w18 in ALLT[17]:
                            for w24 in ALLT[23]:
                                compteur += 1
                                seed = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
                                    W1[0],W2[0],W3[0],W4[0],W5[0],W6[0],W7[0],
                                    w8,
                                    W9[0],
                                    w10,w11,
                                    W12[0],W13[0],W14[0],W15[0],W16[0],
                                    w17,w18,
                                    W19[0],W20[0],W21[0],W22[0],W23[0],
                                    w24
                                )

                                try:
                                    #mm_addr = web3_eth.eth.account.from_mnemonic(seed, account_path=MM_DERIVATION).address
                                    lg_addr = web3_eth.eth.account.from_mnemonic(seed, account_path=LG_DERIVATION).address
                                    
                                    done = False
                                    while not done:
                                        try:
                                            # eth_mm_balance = web3_eth.eth.get_balance(mm_addr) / (10**18)
                                            # pol_mm_balance = web3_pol.eth.get_balance(mm_addr) / (10**18)

                                            eth_lg_balance = web3_eth.eth.get_balance(lg_addr) / (10**18)
                                            pol_lg_balance = web3_pol.eth.get_balance(lg_addr) / (10**18)
                                            done = True
                                        except:
                                            pass
                                    
                                    if(
                                        #    eth_mm_balance
                                        # or pol_mm_balance
                                        # or eth_lg_balance
                                        eth_lg_balance
                                        or pol_lg_balance
                                    ):
                                        with open(LOGFILE, "a") as file:
                                            file.write(seed+"\n")
                                            # file.write(str(mm_addr)+"\n")
                                            file.write(str(lg_addr)+"\n")
                                        
                                except eth_utils.exceptions.ValidationError as err:
                                    pass

with open(LOGFILE, "a") as file:

    file.write("Compteur boucle: " + str(compteur) + "\n")
    file.write("Endtime: " + str(datetime.now()) + "\n")
