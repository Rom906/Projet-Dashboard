import streamlit as st
import pandas as pd


class Page_donnees:
    def __init__(self):
        self.titre = "Visualisation des données"
        self.data = None
        self.load_data("donnees.csv")

    def load_data(self, fichier=""):
        """Charge les données depuis le fichier CSV"""
        try:
            self.data = pd.read_csv(fichier)
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")
            self.data = None

    def get_data_slice(self, l1, l2, c1, c2):
        """Récupère une portion du DataFrame entre les lignes l1 et l2 et les colonnes c1 et c2

        Args:
            l1 (int): Index de la première ligne
            l2 (int): Index de la dernière ligne
            c1 (int): Index de la première colonne
            c2 (int): Index de la dernière colonne

        Returns:
            tuple: (DataFrame sélectionné, liste des noms de colonnes)
        """
        if self.data is not None:
            # Vérifier que les indices sont valides
            max_rows, max_cols = self.data.shape
            l1 = max(0, min(l1, max_rows - 1))
            l2 = max(0, min(l2, max_rows))
            c1 = max(0, min(c1, max_cols - 1))
            c2 = max(0, min(c2, max_cols))

            # Sélectionner la portion du DataFrame
            selected_data = self.data.iloc[l1:l2, c1:c2]
            column_names = selected_data.columns.tolist()

            return selected_data, column_names
        return None, []

    def afficher_page(self):
        """Affiche la page avec les données"""
        st.title(self.titre)

        if self.data is not None:
            # Afficher un aperçu des informations sur le DataFrame
            st.subheader("Aperçu des données")
            st.write(f"Nombre total de lignes : {len(self.data)}")
            st.write(f"Colonnes disponibles : {', '.join(self.data.columns)}")

            # Afficher les données dans un tableau interactif
            st.subheader("Tableau de données")
            st.dataframe(self.data)

            # Ajouter des statistiques de base
            st.subheader("Statistiques descriptives")
            st.write(self.data.describe())
        else:
            st.warning("Aucune donnée n'a été chargée.")
