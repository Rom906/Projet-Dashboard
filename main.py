import streamlit as st
from page_donnees import Page_donnees
from page_graphiques import Graphiques

st.set_page_config(page_title="Dashboard", layout="wide")

données = Page_donnees()
données.load_data("donnees.csv")

st.sidebar.title("Dashboard test Julien Téo")
st.sidebar.subheader("Navigation")
page = st.sidebar.selectbox("Choisir une page", ["Données", "Graphiques"])

st.sidebar.subheader("Options générales")

colonnes = données.data.columns.tolist() if données.data is not None else []
columns_selected_graph_1 = st.sidebar.multiselect(
    "Sélectionner les colonnes à afficher pour le graphique 1", options=colonnes, default=[données.data.columns[0]] if données.data is not None and not données.data.empty else []
)

columns_selected_graph_2 = st.sidebar.multiselect(
    "Sélectionner les colonnes à afficher pour le graphique 2", options=colonnes, default=[données.data.columns[1]] if données.data is not None and len(données.data.columns) > 1 else []
)

data_graph_1 = données.get_columns(columns_selected_graph_1)
data_graph_2 = données.get_columns(columns_selected_graph_2)
graphiques = Graphiques((data_graph_1, data_graph_2))  # type: ignore

if page == "Données":
    données.afficher_page()
else:
    graphiques.render()
