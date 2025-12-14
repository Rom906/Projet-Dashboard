import pandas as pd
import numpy as np


def get_meilleur_coeff_corrélation(mnms, données, délaimax=0):

    couleurs = ["jaune ", "rouge ", "bleu ", "vert ", "marron ", "orange "]
    # gestion date pour mnms
    mnms["date "] = pd.to_datetime(mnms["date "], format="%d/%m/%Y")
    mnms["date "] = mnms["date "].dt.strftime("%d-%m-%Y")

    # gestion date pour les données
    données["timeOpen"] = pd.to_datetime(données["timeOpen"])

    # création nouvelle colonne avec le prix moyen
    données["prix_moyen"] = données[["open", "high", "low", "close"]].mean(axis=1)

    # création du nouveau tableau consitué de la date et du prix moyen uniquement
    dateprix = données[["timeOpen", "prix_moyen"]]
    dateprix["timeOpen"] = dateprix["timeOpen"].dt.strftime("%d-%m-%Y")
    dateprix = dateprix.rename(columns={"timeOpen": "date "})

    # calcul du coeff du meilleur coefficient de correlation pour tous les délais entre 0 et délaimax

    coeffprime = {"délai": 0, "couleur": "", "valeur": 0}

    for i in range(0, délaimax + 1):

        # Décaler le prix moyen d'un jour vers le haut
        dateprix["prix_moyen_t+i"] = dateprix["prix_moyen"].shift(-i)

        # Garder uniquement les colonnes utiles
        resultat = dateprix[["date ", "prix_moyen_t+i"]]

        # création du dictionnaire
        dico_correlation2 = {}
        for coul in couleurs:
            jointure = pd.merge(
                resultat, mnms[["date ", coul]], on="date ", how="right"
            )  # Jointure des données et des mnms sur la colonne 'date'
            X_prix = np.array(jointure["prix_moyen_t+i"])  # vecteur des prix
            X_nbrcouleur = np.array(
                jointure[coul]
            )  # vecteur du nombre de présence de cette couleur dans le paquet
            X_date = np.array(jointure["date "])  # vecteur date
            dico_correlation2[coul] = {
                "date": X_date,
                "prix": X_prix,
                "nombre": X_nbrcouleur,
            }

        # calcul du meilleur coefficient entre les couleurs pour la corrélation correspondante au délai i

        coeffprime_i = {"couleur": "", "valeur": 0}
        for coul in dico_correlation2:

            # calcul des moyennes, de la covariance et de la variance
            X1 = dico_correlation2[coul]["prix"]
            X2 = dico_correlation2[coul]["nombre"]
            X1bar = 1 / X1.size * np.sum(X1)
            X2bar = 1 / X2.size * np.sum(X2)
            varX1 = 1 / X1.size * np.sum((X1 - X1bar) ** 2)
            varX2 = 1 / X2.size * np.sum((X2 - X2bar) ** 2)
            cov = 1 / X1.size * np.sum((X1 - X1bar) * (X2 - X2bar))

            # calcul du coeff de corrélation
            coeff = cov / (np.sqrt(varX2) * np.sqrt(varX1))
            if np.abs(coeff) > coeffprime_i["valeur"]:
                coeffprime_i["couleur"] = coul
                coeffprime_i["valeur"] = coeff

        # vérification si amélioration de la valeur du coeff global (coeffprime)

        if np.abs(coeffprime_i["valeur"]) > np.abs(coeffprime["valeur"]):
            coeffprime["valeur"] = coeffprime_i["valeur"]
            coeffprime["couleur"] = coeffprime_i["couleur"]
            coeffprime["délai"] = i

    print(
        "le meilleur coeff de corrélation est :",
        coeffprime["valeur"],
        "pour la couleur :",
        coeffprime["couleur"],
        "et le délai :",
        coeffprime["délai"],
    )

mnms = pd.read_csv("Données_M&Ms.csv", sep=",")
bitcoin = pd.read_csv(
    "vrai_données_bitcoin.csv", sep=";"
)
etherum = pd.read_csv("données_etherum.csv", sep=";")
solana = pd.read_csv("solana.csv", sep=";")
cardano = pd.read_csv("cardano.csv", sep=";")
dogecoin = pd.read_csv("dogecoin.csv", sep=";")
bitcoincash = pd.read_csv("bitcoincash.csv", sep=';')
zcash = pd.read_csv("zcash.csv", sep=';')
stellar = pd.read_csv("stellar.csv", sep=';') #-0.214 !!!!
get_meilleur_coeff_corrélation(mnms, stellar, 200)

'''crypto = [(bitcoin, 'bitcoin'), (etherum, 'etherum'), (solana, 'solana'), (cardano, 'cardano'), (dogecoin, 'dogecoin'), (bitcoincash, 'bitcoincash'), (zcash, 'zcash'), (stellar, 'stellar')]
for c in crypto :
    print("pour la crypto", c[1], "voici le résultat :")
    get_meilleur_coeff_corrélation(mnms, c[0], 200)'''
