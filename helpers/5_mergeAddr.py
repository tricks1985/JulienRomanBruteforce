maticAddrs = []
ethAddrs = []

with open('4_noMATICBalance.txt') as file:
    addrs = file.readlines()

for addr in addrs:
    maticAddrs += [addr.replace("\n","")]

with open("4bis_noMATICBalance.txt", "r") as file:
    addrs = file.readlines()

for addr in addrs:
    ethAddrs += [addr.replace("\n","")]


# merge addrs with a matic balance on Ethereum OR polygon
for addr in maticAddrs:
    if addr not in ethAddrs:
        ethAddrs += [addr]

ethAddrs.sort(key=str.casefold)

with open("./5_merged.txt", "a") as file:
    for addr in ethAddrs:
        file.write(addr+"\n")
