import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

couleurs = [
    "jaune ",
    "rouge ",
    "bleu ",
    "vert ",
    "marron ",
    "orange ",
]  # l'espace est nécessaire car comme ca dans le fichier csv
dicocouleurs = {}

# --------------------------------

# gestion des données sur les mnms :

mnms = pd.read_csv("Données_M&Ms.csv", sep=",")
mnms["date "] = pd.to_datetime(mnms["date "], format="%d/%m/%Y")
mnms["date "] = mnms["date "].dt.strftime(
    "%d-%m-%Y"
)  # pour mettre les dates dans le bon format
print("taille a la lecture", len(mnms))
# --------------------------------

# gestion du tableau des données du bitcoin

tableau = pd.read_csv(
    "vrai_données_bitcoin.csv", sep=";"
)
tableau["timeOpen"] = pd.to_datetime(tableau["timeOpen"])
tableau["prix_moyen"] = tableau[["open", "high", "low", "close"]].mean(
    axis=1
)  # Calcul du prix moyen de la journée
bitcoin = tableau[
    ["timeOpen", "prix_moyen"]
]  # Créer un DataFrame avec seulement la date et le prix moyen
bitcoin["timeOpen"] = bitcoin["timeOpen"].dt.strftime(
    "%d-%m-%Y"
)  # Reformater la date en DD-MM-YYYY
bitcoin = bitcoin.rename(
    columns={"timeOpen": "date "}
)  # renommage de la colonne pour la jointure


# --------------------------------
# objectif : créé un dictionnaire associe à chaque couleur, le tableau (date d'ouverture du paquet, prix du bitcoin, nombre de mnms de cette couleur dans ce paquet)

dico_correlation = {}
for coul in couleurs:
    jointure = pd.merge(
        bitcoin, mnms[["date ", coul]], on="date ", how="right"
    )  # Jointure de bitcoin et mnms sur la colonne 'date'
    print("la taille de la jointure est", len(jointure))
    dico_correlation[coul] = jointure

for coul in couleurs :
    X_prix = np.array(dico_correlation[coul]["prix_moyen"]) # vecteur des prix
    X_nbrcouleur = np.array(dico_correlation[coul][coul]) # vecteur du nombre de présence de cette couleur dans le paquet
    X_date = np.array(dico_correlation[coul]['date ']) # vecteur date
    dico_correlation[coul] = {'date': X_date, 'prix': X_prix, 'nombre' : X_nbrcouleur}

#__________________________________________

# regression linéaire du module scipy.stats :

#___________________________________________

'''u1, u0, rho, p, stderr = linregress(dico_correlation['orange ']['prix'], dico_correlation['orange ']['nombre'])

plt.figure()
plt.xlabel("prix du bitcoin")
plt.ylabel("nombre de mnms orange")
plt.plot(dico_correlation['orange ']['prix'], dico_correlation['orange ']['nombre'], 'o', label = 'nombre de mnms en fonction du prix du bitcoin')
plt.plot(dico_correlation['orange ']['prix'], u0 + u1 * dico_correlation['orange ']['prix'], 'r-', label='régression linéaire')
plt.legend()
plt.show()'''

# calcul du coefficient de corrélation
coeffprime = ('', 0)
for coul in dico_correlation:
    X1 = dico_correlation[coul]['prix']
    X2 = dico_correlation[coul]['nombre']
    X1bar = 1/X1.size*np.sum(X1)
    X2bar = 1/X2.size*np.sum(X2)
    varX1 = 1/X1.size*np.sum((X1-X1bar)**2)
    varX2 = 1/X2.size*np.sum((X2-X2bar)**2)
    cov = 1/X1.size*np.sum((X1-X1bar)*(X2-X2bar))
    coeff = cov/(np.sqrt(varX2)*np.sqrt(varX1))
    if np.abs(coeff) > coeffprime[1] :
        coeffprime = (coul, coeff)
    print("le coeff de corrélation de", coul, "est :", coeff)

print("le meilleur coeff de corrélation est :", coeffprime[1], "pour la couleur :", coeffprime[0])

#--------------------------

fig, ax1 = plt.subplots(figsize=(10,5))

# Axe Y pour le Bitcoin
ax1.plot(dico_correlation['orange ']["date"], dico_correlation['orange ']["prix"], color="blue", label="Bitcoin (prix moyen)")
ax1.set_xlabel("Date")
ax1.set_ylabel("Prix moyen Bitcoin", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Axe Y secondaire pour les M&Ms
ax2 = ax1.twinx()
ax2.plot(dico_correlation['orange ']["date"], dico_correlation['orange ']["nombre"], 'o', color="orange", label="M&Ms orange")
ax2.set_ylabel("Nombre de M&Ms orange", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")

# Ajouter une légende combinée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Bitcoin vs M&Ms orange")
plt.show()

#-----------------------------------

'''plt.figure()
plt.xlabel('nombre de orange')
plt.ylabel('prix du bitcoin')
plt.plot(x, dico_correlation['orange ']['nombre'], '-r', label= 'évolution du bitcoin en fonction des temps douverture de paquet')
plt.plot(x, dico_correlation['orange ']['prix'], '-b', label ='évolution du nombre de mnms par paquet en fonction des dates douvertures')
plt.legend()
plt.show()'''


