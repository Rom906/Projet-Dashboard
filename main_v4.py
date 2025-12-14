import streamlit as st
from page_donnees_V3 import Page_donnees_v3
from page_graphique_v4 import Graphiques, Area
from typing import Dict
from systeme_sauvegarde import save


st.set_page_config(page_title="Dashboard", layout="wide")


def safe_rerun() -> None:
    """Appelle st.experimental_rerun() quand l'application est lancée par
    Streamlit; ignore proprement l'appel quand le script est exécuté avec
    `python main_V3.py` (mode "bare"), empêchant une exception non souhaitée.
    """
    try:
        st.rerun()
    except Exception:
        # Si on est hors du contexte Streamlit (par ex. execution directe
        # avec `python main_V3.py`), on ignore silencieusement le rerun.
        return


if "graphiques" not in st.session_state:
    st.session_state.graphiques = Graphiques()

if "données" not in st.session_state:
    st.session_state.données = Page_donnees_v3()

# NE PAS créer de références locales - toujours utiliser st.session_state directement


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
        elif titre_nouvelle_ligne in st.session_state.graphiques.get_lines_titles():
            st.text("Il y a déjà une ligne ayant ce nom")
        else:
            st.session_state.graphiques.add_line(
                titre_nouvelle_ligne, afficher_titre_ligne
            )
            # forcer un rerun pour mettre à jour l'affichage immédiatement
            safe_rerun()

    st.subheader("Ajouter une zone graphique")
    if st.session_state.graphiques.lines != []:
        titre_ligne_modifiée = st.selectbox(
            "Selectionnez la ligne dans laquelle vous allez rajouter la zone",
            st.session_state.graphiques.get_lines_titles(),
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
                line_index = st.session_state.graphiques.get_line_index(
                    titre_ligne_modifiée
                )
                if line_index is None:
                    st.error("Erreur interne, voir développeurs")
                st.session_state.graphiques.add_area(line_index, titre_nouvelle_zone, type_graphique, show_name=afficher_titre_zone)  # type: ignore
                # forcer un rerun pour que la nouvelle zone soit rendue
                safe_rerun()

# Retirer des lignes et des colonnes

with st.sidebar.expander("Retirer des zones"):
    lines_names = st.session_state.graphiques.get_lines_titles()

    st.subheader("Supprimer une ligne")
    ligne_supprimée = st.selectbox("Choisissez la ligne à supprimer", lines_names)
    if st.button("Supprimer la ligne"):
        st.session_state.graphiques.delete_line(ligne_supprimée)
        lines_names.remove(ligne_supprimée)
        safe_rerun()

    st.subheader("Retirer une zone graphique")
    ligne_selectionnée = st.selectbox(
        "Séléctionnez la ligne contenant la zone à supprimer", lines_names
    )
    if ligne_selectionnée:
        areas_name = st.session_state.graphiques.get_line_areas_names(
            ligne_selectionnée
        )
        area_supprimée = st.selectbox("Choisissez la zone à supprimer", areas_name)
        if st.button("Supprimer la zone"):
            st.session_state.graphiques.delete_area(ligne_selectionnée, area_supprimée)
            areas_name.remove(area_supprimée)
            safe_rerun()

# Choix de la ligne et de la zone dans laquelle on modifie les graphiques

with st.sidebar.expander("Gestion des données graphiqes"):
    st.subheader("Choix de la ligne à modifier")
    nom_ligne_modifiée = st.selectbox(
        "Selectionnez la ligne à modifier",
        options=st.session_state.graphiques.get_lines_titles(),
    )
    if "nom_ligne_modifiée" not in st.session_state:
        st.session_state.nom_ligne_modifiée = nom_ligne_modifiée

    if nom_ligne_modifiée:
        st.subheader("Choix de la zone graphique à modifier")
        graphics_names = st.session_state.graphiques.get_line_areas_names(
            nom_ligne_modifiée
        )
        nom_area_modifiée = st.selectbox(
            "Sélectionnez la zone à modifier", options=graphics_names
        )
        if "nom_area_modifiée" not in st.session_state:
            st.session_state.nom_area_modifiée = nom_area_modifiée

        if nom_area_modifiée and nom_ligne_modifiée:
            if "range" not in st.session_state:
                st.session_state.range = st.session_state.graphiques.get_area_range(nom_ligne_modifiée, nom_area_modifiée)
            if (
                nom_ligne_modifiée != st.session_state.nom_ligne_modifiée
                or nom_area_modifiée != st.session_state.nom_area_modifiée
            ):
                st.session_state.nom_ligne_modifiée = nom_ligne_modifiée
                st.session_state.nom_area_modifiée = nom_area_modifiée
                st.session_state.colonnes_affichées_default = (
                    st.session_state.graphiques.get_area_ploted_columns(
                        nom_ligne_modifiée, nom_area_modifiée
                    )
                )
                st.session_state.colonne_abscisse = (
                    st.session_state.graphiques.get_area_abscisse_column_name(
                        nom_ligne_modifiée, nom_area_modifiée
                    )
                )
                st.session_state.range = st.session_state.graphiques.get_area_range(nom_ligne_modifiée, nom_area_modifiée)
            # Vérifier que les données sont disponibles
            st.session_state.graphiques.render_area_sidebar_options(
                nom_ligne_modifiée, nom_area_modifiée
            )

# Sauvegarde
st.sidebar.download_button(
    "Télécharger une sauvegarde",
    data=save(st.session_state.graphiques, st.session_state.données),  # type: ignore
    file_name="Sauvegarde_dashboard.json",
    mime="application/json",
)

# Rendering


if page == "Données":
    st.session_state.données.afficher_page()
else:
    st.session_state.graphiques.render()
