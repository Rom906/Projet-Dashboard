from page_graphique_v4 import Graphiques, Area
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
            if area_courante.content_type == area_courante.MARKDOWN:
                sauvegarde[ligne_courante.title][area_courante.area_name] = {
                    "index": j,
                    "show_name": area_courante.show_name,
                    "content_type": area_courante.content_type,
                    "text": area_courante.text
                }
            else:
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


def load(
    sauvegarde_str: str, page_graphique: Graphiques, page_données: Page_donnees_v3
):
    sauvegarde = json.loads(sauvegarde_str)
    # Restaurer d'abord les données brutes si présentes afin de pouvoir reconstruire
    # les DataFrame des areas ensuite.
    data_dict = sauvegarde.get("data", {})
    if data_dict:
        import pandas as pd

        data_frame = pd.DataFrame(data_dict)
        page_données.data = data_frame
        if data_frame.index.name:
            page_données.data.set_index(data_frame.index.name, inplace=True)
        else:
            page_données.data.index.name = None
    else:
        page_données.data = None

    for ligne_title, ligne_data in sauvegarde.items():
        if ligne_title == "data":
            continue
        # Assurer que l'index de ligne existe ; si non, créer les lignes manquantes
        index = ligne_data.get("index")
        if index is None:
            # ignore malformed entry
            continue
        # créer des lignes jusqu'à l'index demandé
        while index >= len(page_graphique.lines):
            # nom par défaut temporaire, on le remplacera par le titre sauvegardé
            page_graphique.add_line(f"Ligne_{len(page_graphique.lines)}", True)

        ligne_courante = page_graphique.lines[index]
        # mettre à jour le titre et l'affichage
        ligne_courante.title = ligne_title
        ligne_courante.show_title = ligne_data.get("show_title", True)
        for area_name, area_data in ligne_data.items():
            if area_name == "index" or area_name == "show_title":
                continue
            # Assurer que l'index de la zone existe ; sinon créer des zones vides
            area_index = area_data.get("index")
            if area_index is None:
                continue
            while area_index >= len(ligne_courante.areas):
                # créer une area vide avec un nom générique
                ligne_courante.add_area(
                    f"Area_{len(ligne_courante.areas)}",
                    area_data.get("content_type", 4),
                    None,
                )
                if area_data["content_type"] == Area.MARKDOWN:
                    ligne_courante.areas[area_index].text = area_data["text"]
                    ligne_courante.areas[area_index].input_mode = False

            area_courante = ligne_courante.areas[area_index]
            area_courante.area_name = area_name
            area_courante.show_name = area_data.get("show_name", True)
            area_courante.content_type = area_data.get(
                "content_type", area_courante.content_type
            )
            # Restaurer les données de la zone si elles sont présentes dans la sauvegarde
            columns_name = area_data.get("columns_name")
            abscisse_column_name = area_data.get("abscisse_column_name")
            if (
                columns_name
                and page_données is not None
                and page_données.data is not None
            ):
                try:
                    # Utiliser la méthode de Page_donnees_v3 pour construire le DataFrame des colonnes
                    if hasattr(page_données, "get_columns"):
                        df_cols = page_données.get_columns(columns_name)
                    else:
                        # fallback direct
                        df_cols = page_données.data[columns_name].copy()

                    # Si l'abscisse est dans les données globales mais pas dans df_cols,
                    # la réinsérer temporairement afin de pouvoir la mettre en index.
                    if (
                        abscisse_column_name
                        and abscisse_column_name not in df_cols.columns
                        and abscisse_column_name in page_données.data.columns
                    ):
                        df_cols[abscisse_column_name] = page_données.data[
                            abscisse_column_name
                        ]

                    # si abscisse définie, la mettre en index
                    if abscisse_column_name and abscisse_column_name in df_cols.columns:
                        df_cols = df_cols.set_index(abscisse_column_name)

                    area_courante.data = df_cols
                except Exception:
                    # ne pas planter le chargement si reconstruction des données échoue
                    area_courante.data = None

    return page_graphique, page_données
