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

st.sidebar.subheader("Navigation")
page = st.sidebar.selectbox("Choisir une page", ["Données", "Graphiques"])

# Ajouter des lignes

titre_nouvelle_ligne = st.text_input("Entrez le titre de la ligne")
afficher_titre = st.checkbox("Afficher le nom de la ligne en haut de celle-ci")
if st.button("Ajouter une ligne"):
    if titre_nouvelle_ligne:
        st.text("aucun nom de ligne entré")
    elif titre_nouvelle_ligne in graphiques.get_lines_titles():
        st.text("Il y a déjà une ligne ayant ce nom")
    else:
        graphiques.add_line(titre_nouvelle_ligne)


# Choix de la ligne dans laquelle on modifie les graphiques

st.sidebar.subheader("gestion des lignes")
st.sidebar.selectbox("Selectionnez la ligne à modifier", [i for i in range(graphiques.get_lines_count())])

# Choix de la zone graphique que l'on modifie ( le graphique quoi )

st.sidebar.subheader("Choix de la zone graphique")

graphics_names = graphiques.get_areas_names()
area = st.multiselect("Sélectionnez la zone à afficher", options=graphics_names[0], default=graphics_names[0])

st.sidebar.subheader("Choix des paramètres du graphique")

colonnes = données.data.columns.tolist() if données.data is not None else []

columns_selected_graph_2 = st.sidebar.multiselect(
    "Sélectionner les colonnes à afficher pour le graphique 2", options=colonnes, default=[données.data.columns[1]] if données.data is not None and len(données.data.columns) > 1 else []
)


"""
Rendering
"""


if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
