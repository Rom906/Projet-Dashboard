import pandas as pd

def recup_paquet(donnees, i):
    couleurs = ['jaune', 'rouge', 'bleu', 'vert', 'marron', 'orange']
    # Normalise les colonnes
    cols = donnees.columns.str.strip().str.lower()
    donnees = donnees.rename(columns=dict(zip(donnees.columns, cols)))

    if i < 0 or i >= len(donnees):
        raise IndexError(f"Index {i} hors limites (0..{len(donnees)-1})")

    row = donnees.iloc[i]
    result = {}
    for c in couleurs:
        val = row[c] if c in row.index else None
        # Convertis proprement en int quand possible
        if pd.notna(val):
            try:
                result[c] = int(val)
            except (ValueError, TypeError):
                result[c] = val  # garde la valeur brute si ce n'est pas un nombre
        else:
            result[c] = 0  # ou None, selon préférence
    return result


