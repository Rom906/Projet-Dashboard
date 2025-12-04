# Cette fonction renvoit et affiche l'hexagramme du Yi King correspondant à un paquet donné, dont il faut donner le contenu dans le terminal lorsque demandé.
import pandas 

def schema_yi_jing_mut(dict):

    yin = "--   --"
    yang = "-------"
    yin_mutant = "-- x --"
    yang_mutant = "---o---"

    rouge = dict['rouge']
    orange = dict['orange']
    jaune = dict['jaune']
    vert = dict['vert']
    bleu = dict['bleu']
    marron = dict['marron']
    ensemble = [rouge, orange, jaune, vert, bleu, marron]
    total = 0
    for nb in ensemble:
        total += nb
    dessin = []

    for nb_couleur in ensemble:
        sous_tot = total - nb_couleur
        if (nb_couleur % 2) == 0:  # Yin
            if sous_tot % 8 == 0:  # Yin mutant
                dessin.append(yin_mutant)
            else:  # Yin jeune
                dessin.append(yin)
        else:  # Yang
            if (sous_tot % 8) in [1, 2, 3]:  # Yang mutant
                dessin.append(yang_mutant)
            else:  # Yang jeune
                dessin.append(yang)
    return(dessin)

def schema_yi_jing(dict):

    yin = "yin"
    yang = "yang"

    rouge = dict['rouge']
    orange = dict['orange']
    jaune = dict['jaune']
    vert = dict['vert']
    bleu = dict['bleu']
    marron = dict['marron']
    ensemble = [rouge, orange, jaune, vert, bleu, marron]
    total = 0
    for nb in ensemble:
        total += nb
    dessin = []

    for nb_couleur in ensemble:
        sous_tot = total - nb_couleur
        if (nb_couleur % 2) == 0:  # Yin
            dessin.append(yin)
        else:  # Yang
            dessin.append(yang)
    return(dessin)
