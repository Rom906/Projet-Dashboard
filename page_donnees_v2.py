import streamlit as st
import pandas as pd
from typing import List


class Page_donnees_v2:
    def __init__(self):
        self.titre = "Visualisation des données"
        self.data = None

    def load_data(self, fichier=""):
        """Charge les données depuis le fichier CSV"""
        try:
            self.data = pd.read_csv(fichier, sep="\t")
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

            return selected_data
        return None, []

    def get_columns(self, columns_selected_names: List[str]):
        if self.data is not None:
            colonnes = {}
            for column_name in columns_selected_names:
                colonnes[column_name] = self.data[column_name]
            return pd.DataFrame(colonnes)

    def afficher_page(self):
        """Affiche la page avec les données et le drag and drop"""
        st.title(self.titre)

        # Zone de drag and drop pour importer un fichier CSV
        st.subheader("Importer un fichier CSV")
        uploaded_file = st.file_uploader(
            "Glissez-déposez votre fichier CSV ici ou cliquez pour parcourir",
            type="csv",
            label_visibility="collapsed"
        )

        # Traiter le fichier uploadé
        if uploaded_file is not None:
            try:
                # Charger le fichier
                self.data = pd.read_csv(uploaded_file, sep="\t")
                st.session_state.donnees_v2 = self
                st.success("Fichier chargé avec succès!")
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier: {str(e)}")
                # Essayer avec d'autres séparateurs
                try:
                    self.data = pd.read_csv(uploaded_file, sep=",")
                    st.session_state.donnees_v2 = self
                    st.success("Fichier chargé avec succès (séparateur détecté: virgule)!")
                except Exception as e2:
                    st.error(f"Impossible de charger le fichier: {str(e2)}")

        # Afficher les données si elles ont été chargées
        if self.data is not None:
            st.divider()
            
            # Afficher un aperçu des informations sur le DataFrame
            st.subheader("Aperçu des données")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nombre de lignes", len(self.data))
            with col2:
                st.metric("Nombre de colonnes", len(self.data.columns))
            with col3:
                st.metric("Colonnes disponibles", len(self.data.columns))

            # Afficher les colonnes disponibles
            st.write(f"**Colonnes:** {', '.join(self.data.columns)}")

            # Afficher les données dans un tableau interactif
            st.subheader("Tableau de données")
            st.dataframe(self.data, use_container_width=True)

            # Ajouter des statistiques de base
            st.subheader("Statistiques descriptives")
            st.dataframe(self.data.describe(), use_container_width=True)
        else:
            st.info("Aucune donnée n'a été chargée. Veuillez importer un fichier CSV.")
