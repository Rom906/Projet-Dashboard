import streamlit as st
from page_donnees_v2 import Page_donnees_v2
from page_graphique_v2 import Graphiques, Area
from typing import Dict


st.set_page_config(page_title="Dashboard", layout="wide")

if "graphiques" not in st.session_state:
    st.session_state.graphiques = Graphiques()

if "données" not in st.session_state:
    st.session_state.données = Page_donnees_v2()

graphiques = st.session_state.graphiques
données = st.session_state.données


# Sidebar gestion

parameters: Dict = {}

st.sidebar.title("Dashboard test Julien Téo V2")

# Navigation entre les pages

with st.sidebar.expander("Navigation"):
    page = st.selectbox("Choisir une page", ["Données", "Graphiques"])

# Ajouter des lignes et des colonnes

with st.sidebar.expander("Ajouter des zones"):
    st.subheader("Ajouter une ligne")
    titre_nouvelle_ligne = st.text_input("Entrez le titre de la ligne")
    afficher_titre_ligne = st.checkbox("Afficher le titre de la ligne en haut de celle-ci")
    if st.button("Ajouter une ligne"):
        if not titre_nouvelle_ligne:
            st.text("Aucun nom de ligne entré")
        elif titre_nouvelle_ligne in graphiques.get_lines_titles():
            st.text("Il y a déjà une ligne ayant ce nom")
        else:
            graphiques.add_line(titre_nouvelle_ligne, afficher_titre_ligne)

    st.subheader("Ajouter une zone graphique")
    if graphiques.lines != []:
        titre_ligne_modifiée = st.selectbox("Selectionnez la ligne dans laquelle vous allez rajouter la zone", graphiques.get_lines_titles())
        titre_nouvelle_zone = st.text_input("Entrez le titre de la noiuvelle zone")
        afficher_titre_zone = st.checkbox("Afficher le titre de la zone en haut de celle-ci")
        options = Area.get_types()
        type_graphique = st.radio("Choississez le type de graphique à implémenter", options)
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

# Retirer des lignes et des colonnes

with st.sidebar.expander("Retirer des zones"):
    lines_names = graphiques.get_lines_titles()

    st.subheader("Supprimer une ligne")
    ligne_supprimée = st.selectbox("Choisissez la ligne à supprimer", lines_names)
    if st.button("Supprimer la ligne"):
        graphiques.delete_line(ligne_supprimée)
        lines_names.remove(ligne_supprimée)

    st.subheader("Retirer une zone graphique")
    ligne_selectionnée = st.selectbox("Séléctionnez la ligne contenant la zone à supprimer", lines_names)
    if ligne_selectionnée:
        areas_name = graphiques.get_line_areas_name(ligne_selectionnée)
        area_supprimée = st.selectbox("Choisissez la zone à supprimer", areas_name)
        if st.button("Supprimer la zone"):
            graphiques.delete_area(ligne_selectionnée, area_supprimée)
            areas_name.remove(area_supprimée)

# Choix de la ligne et de la zone dans laquelle on modifie les graphiques

with st.sidebar.expander("Gestion des données graphiqes"):
    st.subheader("Choix de la ligne à modifier")
    nom_ligne_modifiée = st.selectbox("Selectionnez la ligne à modifier", options=graphiques.get_lines_titles())

    st.subheader("Choix de la zone graphique à modifier")
    graphics_names = graphiques.get_areas_names()
    nom_area_modifié = st.selectbox("Sélectionnez la zone à modifier", options=graphics_names)

    if nom_area_modifié and nom_ligne_modifiée:
        st.subheader("Paramètres du graphique")
        st.subheader("Choix des données")
        colonnes_données = données.data.columns.to_list()  # type: ignore
        colonnes_deja_séléctionnées = graphiques.get_area_ploted_columns(nom_ligne_modifiée, nom_area_modifié)
        colonnes_affichées = st.multiselect("Choississez les colonnes utilisées dans le graphique", colonnes_données, default=colonnes_deja_séléctionnées)
        données_affichées = données.get_columns(colonnes_affichées)
        graphiques.set_datas(nom_ligne_modifiée, nom_area_modifié, données_affichées)  # type: ignore

        st.subheader("Choix de l'axe d'abcisse")
        colonne_abscisse = st.selectbox("Séléctionnez la colonne à mettre en axe des abscisses", [""] + colonnes_affichées)
        graphiques.set_area_abscisse_column(nom_ligne_modifiée, nom_area_modifié, colonne_abscisse)

# Rendering


if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
