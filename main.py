from genere_hexagramme import recup_paquet
import pandas as pd
from yi_king import schema_yi_jing
from ki2 import test_khi2

donnees = pd.read_csv('Données_M&Ms.csv')

L = []
for i in range(len(donnees.index)):
    L.append(schema_yi_jing(recup_paquet(donnees, i)))

d1 = donnees.assign(hexagramme=L)
#print(d1)

hexadict = {}
for l in L:
    hexadict[str(l)] = 0
for l in L:
    hexadict[str(l)] +=1

x2calc = 0
for h in hexadict:
    x2calc += (hexadict[h]-len(donnees)/64)**2/(len(donnees)/64)
print(x2calc)

obs = [hexadict[h] for h in hexadict]
theo = [len(donnees)/64 for _ in range(len(hexadict))]

print(test_khi2(63, obs, theo))