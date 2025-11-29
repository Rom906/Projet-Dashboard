import streamlit as st
from page_donnees_V3 import Page_donnees_v3
from page_graphique_V3 import Graphiques, Area
from typing import Dict
from systeme_sauvegarde import save


st.set_page_config(page_title="Dashboard", layout="wide")


def safe_rerun() -> None:
    """Appelle st.experimental_rerun() quand l'application est lancée par
    Streamlit; ignore proprement l'appel quand le script est exécuté avec
    `python main_V3.py` (mode "bare"), empêchant une exception non souhaitée.
    """
    try:
        st.experimental_rerun()
    except Exception:
        # Si on est hors du contexte Streamlit (par ex. execution directe
        # avec `python main_V3.py`), on ignore silencieusement le rerun.
        return


if "graphiques" not in st.session_state:
    st.session_state.graphiques = Graphiques()

if "données" not in st.session_state:
    st.session_state.données = Page_donnees_v3()

graphiques = st.session_state.graphiques
données = st.session_state.données


# Sidebar gestion

parameters: Dict = {}

st.sidebar.title("Dashboard test Julien Téo Romain V3")

# Navigation entre les pages

with st.sidebar.expander("Navigation"):
    page = st.selectbox("Choisir une page", ["Données", "Graphiques"])
    # stocker la page sélectionnée dans la session pour qu'elle soit accessible
    # depuis d'autres modules (par ex. page_donnees_V3.afficher_page)
    st.session_state["page"] = page

# Ajouter des lignes et des colonnes

with st.sidebar.expander("Ajouter des zones"):
    st.subheader("Ajouter une ligne")
    titre_nouvelle_ligne = st.text_input("Entrez le titre de la ligne")
    afficher_titre_ligne = st.checkbox(
        "Afficher le titre de la ligne en haut de celle-ci"
    )
    if st.button("Ajouter une ligne"):
        if not titre_nouvelle_ligne:
            st.text("Aucun nom de ligne entré")
        elif titre_nouvelle_ligne in graphiques.get_lines_titles():
            st.text("Il y a déjà une ligne ayant ce nom")
        else:
            graphiques.add_line(titre_nouvelle_ligne, afficher_titre_ligne)
            # forcer un rerun pour mettre à jour l'affichage immédiatement
            safe_rerun()

    st.subheader("Ajouter une zone graphique")
    if graphiques.lines != []:
        titre_ligne_modifiée = st.selectbox(
            "Selectionnez la ligne dans laquelle vous allez rajouter la zone",
            graphiques.get_lines_titles(),
        )
        titre_nouvelle_zone = st.text_input("Entrez le titre de la noiuvelle zone")
        afficher_titre_zone = st.checkbox(
            "Afficher le titre de la zone en haut de celle-ci"
        )
        options = Area.get_types()
        type_graphique = st.radio(
            "Choississez le type de graphique à implémenter", options
        )
        if st.button("Ajouter une zone"):
            if not titre_ligne_modifiée:
                st.error("Vous n'avez pas entré de ligne à modifier")
            if not titre_nouvelle_zone:
                st.error("Vous n'avez pas entré de nom pour la nouvelle zone")
            if not type_graphique:
                st.error("Aucun type de graphique séléctionné")
            else:
                line_index = graphiques.get_line_index(titre_ligne_modifiée)
                if line_index is None:
                    st.error("Erreur interne, voir développeurs")
                graphiques.add_area(line_index, titre_nouvelle_zone, type_graphique, show_name=afficher_titre_zone)  # type: ignore
                # forcer un rerun pour que la nouvelle zone soit rendue
                safe_rerun()

# Retirer des lignes et des colonnes

with st.sidebar.expander("Retirer des zones"):
    lines_names = graphiques.get_lines_titles()

    st.subheader("Supprimer une ligne")
    ligne_supprimée = st.selectbox("Choisissez la ligne à supprimer", lines_names)
    if st.button("Supprimer la ligne"):
        graphiques.delete_line(ligne_supprimée)
        lines_names.remove(ligne_supprimée)
        safe_rerun()

    st.subheader("Retirer une zone graphique")
    ligne_selectionnée = st.selectbox(
        "Séléctionnez la ligne contenant la zone à supprimer", lines_names
    )
    if ligne_selectionnée:
        areas_name = graphiques.get_line_areas_names(ligne_selectionnée)
        area_supprimée = st.selectbox("Choisissez la zone à supprimer", areas_name)
        if st.button("Supprimer la zone"):
            graphiques.delete_area(ligne_selectionnée, area_supprimée)
            areas_name.remove(area_supprimée)
            safe_rerun()

# Choix de la ligne et de la zone dans laquelle on modifie les graphiques

with st.sidebar.expander("Gestion des données graphiqes"):
    st.subheader("Choix de la ligne à modifier")
    nom_ligne_modifiée = st.selectbox(
        "Selectionnez la ligne à modifier", options=graphiques.get_lines_titles()
    )
    if "nom_ligne_modifiée" not in st.session_state:
        st.session_state.nom_ligne_modifiée = nom_ligne_modifiée

    if nom_ligne_modifiée:
        st.subheader("Choix de la zone graphique à modifier")
        graphics_names = graphiques.get_line_areas_names(nom_ligne_modifiée)
        nom_area_modifié = st.selectbox(
            "Sélectionnez la zone à modifier", options=graphics_names
        )
        if "nom_area_modifiée" not in st.session_state:
            st.session_state.nom_area_modifiée = nom_area_modifié

        if nom_area_modifié and nom_ligne_modifiée:
            st.subheader("Paramètres du graphique")
            st.subheader("Choix des données")
            colonnes_données = données.data.columns.to_list()  # type: ignore
            if "colonnes_affichées_default" not in st.session_state:
                st.session_state.colonnes_affichées_default = graphiques.get_area_ploted_columns(
                    nom_ligne_modifiée, nom_area_modifié
                )
            if st.session_state.nom_area_modifiée != nom_area_modifié or nom_ligne_modifiée != st.session_state.nom_ligne_modifiée:
                st.session_state.nom_area_modifiée = nom_area_modifié
                st.session_state.nom_ligne_modifiée = nom_ligne_modifiée
                st.session_state.colonnes_affichées_default = graphiques.get_area_ploted_columns(
                    nom_ligne_modifiée, nom_area_modifié
                )
            temp_données_affichées = st.multiselect(
                "Choississez les colonnes utilisées dans le graphique",
                colonnes_données,
                key="colonnes_affichées_default",
            )
            données_affichées = données.get_columns(temp_données_affichées)
            graphiques.set_datas(nom_ligne_modifiée, nom_area_modifié, données_affichées)  # type: ignore

            st.subheader("Choix de l'axe des abscisses")
            colonne_abscisse = st.selectbox(
                "Séléctionnez la colonne à mettre en axe des abscisses",
                [""] + temp_données_affichées,
            )
            if colonne_abscisse:
                graphiques.set_area_abscisse_column(
                    nom_ligne_modifiée, nom_area_modifié, colonne_abscisse
                )

# Sauvegarde
st.sidebar.download_button(
    "Télécharger une sauvegarde",
    data=save(graphiques, données),
    file_name="Sauvegarde_dashboard.json",
    mime="application/json",
)

# Rendering


if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
