from bip_utils import *
import json

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[413,429,495,500,502,503,504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

URL = "https://blockchain.info/rawaddr/"

def get_addr_from_mnemo(mnemonic):

    # Generate from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Derivation path returned: m
    bip_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    bip_acc_ctx = bip_mst_ctx.Purpose().Coin().Account(0)
    bip_chg_ctx = bip_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    bip_addr_ctx = bip_chg_ctx.AddressIndex(0)
    bip_addr = bip_addr_ctx.PublicKey().ToAddress()

    return bip_addr

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
W17 = ['clean']
W18 = ['clap']
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
not_sure = [7,8,9,10,11,12,17,18,19,20,21,22,23,24]
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
                                                            is_valid = Bip39MnemonicValidator().IsValid(seed)

                                                            if is_valid:
                                                                url = URL+get_addr_from_mnemo(seed)
                                                                response = requests.get(url)
                                                                body = json.loads(response.content)
                                                                print(body)
                                                                n_tx = body['n_tx']
                                                                if n_tx:
                                                                    print(seed)


print(compteur)