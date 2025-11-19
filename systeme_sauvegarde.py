from page_graphique_V3 import Graphiques
from page_donnees_V3 import Page_donnees_v3
import json


def save(page_graphique: Graphiques, page_données: Page_donnees_v3):
    sauvegarde = {}
    lignes = page_graphique.lines
    for i in range(len(lignes)):
        ligne_courante = lignes[i]
        areas = ligne_courante.areas
        sauvegarde[ligne_courante.title] = {
            "index": i,
            "show_title": ligne_courante.show_title,
        }
        for j in range(len(areas)):
            area_courante = areas[j]
            data = area_courante.data
            sauvegarde[ligne_courante.title][area_courante.area_name] = {
                "index": j,
                "show_name": area_courante.show_name,
                "content_type": area_courante.content_type,
            }
            if data is not None:
                sauvegarde[ligne_courante.title][area_courante.area_name][
                    "columns_name"
                ] = data.columns.to_list()
                sauvegarde[ligne_courante.title][area_courante.area_name][
                    "abscisse_column_name"
                ] = data.index.name

    data = page_données.data
    sauvegarde["data"] = {}
    if data is not None:
        for name in data.columns.to_list():
            sauvegarde["data"][name] = data[name].to_list()
    return json.dumps(sauvegarde, indent=4, ensure_ascii=False)
