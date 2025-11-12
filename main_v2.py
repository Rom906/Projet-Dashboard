import streamlit as st
from page_donnees import Page_donnees
from page_graphique_v2 import Graphiques, Area
from typing import Dict


st.set_page_config(page_title="Dashboard", layout="wide")


données = Page_donnees()
graphiques = Graphiques()
données.load_data("donnees.csv")


"""
Sidebar gestion
"""

parameters: Dict = {}

st.sidebar.title("Dashboard test Julien Téo V2")

# Navigation entre les pages

with st.sidebar.expander("Navigation"):
    page = st.sidebar.selectbox("Choisir une page", ["Données", "Graphiques"])

# Ajouter des lignes et des colonnes

with st.sidebar.expander("Gestion de l'affichage"):
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

# Choix de la ligne et de la zone dans laquelle on modifie les graphiques

with st.sidebar.expander("Gestion des graphiques"):
    st.sidebar.subheader("Choix de la ligne à modifier")
    nom_ligne_modifiée = st.sidebar.selectbox("Selectionnez la ligne à modifier", options=graphiques.get_lines_titles())

    st.sidebar.subheader("Choix de la zone graphique à modifier")
    graphics_names = graphiques.get_areas_names()
    noms_graphique_modifiés = st.multiselect("Sélectionnez la zone à modifier", options=graphics_names, default=graphics_names[0] if graphics_names != [] else None)

    if noms_graphique_modifiés and nom_ligne_modifiée:
        st.sidebar.subheader("Paramètres du graphique")
        st.subheader("choix des données")
        colonnes_données = données.data.columns.to_list()  # type: ignore
        colonnes_affichées = st.multiselect("Choississez les colonnes mises en ordonnée du graphique", colonnes_données)
        données_affichées = données.get_columns(colonnes_affichées)
        for nom_graphique_modifié in noms_graphique_modifiés:
            graphiques.set_datas(nom_ligne_modifiée, nom_graphique_modifié, données_affichées)  # type: ignore


"""
Rendering
"""


if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
