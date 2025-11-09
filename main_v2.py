import streamlit as st
from page_donnees import Page_donnees
from page_graphique_v2 import Graphiques
from utils import Parameters
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

# Ajouter des lignes

with st.sidebar.expander("Gestion de l'affichage"):
    titre_nouvelle_ligne = st.text_input("Entrez le titre de la ligne")
    afficher_titre = st.checkbox("Afficher le nom de la ligne en haut de celle-ci")
    if st.button("Ajouter une ligne"):
        if titre_nouvelle_ligne:
            st.text("aucun nom de ligne entré")
        elif titre_nouvelle_ligne in graphiques.get_lines_titles():
            st.text("Il y a déjà une ligne ayant ce nom")
        else:
            graphiques.add_line(titre_nouvelle_ligne)


# Choix de la ligne et de la zone dans laquelle on modifie les graphiques

with st.sidebar.expander("Gestion des graphiques"):
    st.sidebar.subheader("Choix de la ligne à modifier")
    st.sidebar.selectbox("Selectionnez la ligne à modifier", [i for i in range(graphiques.get_lines_count())])

    st.sidebar.subheader("Choix de la zone graphique à modifier")
    graphics_names = graphiques.get_areas_names()
    area = st.multiselect("Sélectionnez la zone à afficher", options=graphics_names[0], default=graphics_names[0])

    st.sidebar.subheader("Choix des paramètres du graphique")
    colonnes = données.data.columns.tolist() if données.data is not None else []
    abcisse = st.sidebar.selectbox("Selectionnez la colonne d'abcisse", options=colonnes)
    options_slider = données.data[abcisse]  # type: ignore
    columns_selected_graph_2 = st.sidebar.multiselect(
        "Sélectionner les colonnes à afficher pour le graphique", options=colonnes, default=[données.data.columns[1]] if données.data is not None and len(données.data.columns) > 1 else []
    )


"""
Rendering
"""


if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
