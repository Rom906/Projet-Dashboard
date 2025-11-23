import os
import sys
import pandas as pd

# S'assurer que le répertoire parent (projet) est dans sys.path pour permettre
# les imports locaux même quand le script est exécuté depuis le dossier tests.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from page_graphique_V3 import Graphiques, Area
from page_donnees_V3 import Page_donnees_v3
from systeme_sauvegarde import save, load


def run_test():
    # Préparer les données
    df = pd.DataFrame({"x": [1, 2, 3], "a": [10, 20, 30], "b": [5, 6, 7]})

    page_donnees = Page_donnees_v3()
    page_donnees.data = df

    graphiques = Graphiques()
    graphiques.add_line("L1", True)
    # ajouter une area (type en string accepté)
    graphiques.add_area(0, "Area1", "Histogramme", None)

    # sélectionner les colonnes x, a et b pour l'area (x sera ensuite utilisé comme abscisse)
    données_affichées = page_donnees.get_columns(["x", "a", "b"])  # DataFrame avec colonnes x, a, b
    graphiques.set_datas("L1", "Area1", données_affichées)
    # Définir x comme abscisse (déplacera la colonne x vers l'index)
    graphiques.set_area_abscisse_column("L1", "Area1", "x")

    # Sauvegarder
    sauvegarde_str = save(graphiques, page_donnees)

    # Charger dans de nouvelles instances
    graphiques2 = Graphiques()
    page_donnees2 = Page_donnees_v3()
    graphiques2, page_donnees2 = load(sauvegarde_str, graphiques2, page_donnees2)

    # Vérifier que les colonnes tracées pour l'area sont a et b
    cols = graphiques2.get_area_ploted_columns("L1", "Area1")
    print("Cols après chargement:", cols)
    assert cols == ["a", "b"], f"Colonnes restaurées incorrectes: {cols}"


if __name__ == "__main__":
    run_test()
