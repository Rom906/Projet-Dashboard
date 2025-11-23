import streamlit as st
import pandas as pd
from typing import List
import csv
import io
import re


class Page_donnees_v3:
    def __init__(self):
        self.titre = "Visualisation des données"
        self.data = None

    def load_data(self, fichier=""):
        """Charge les données depuis le fichier CSV"""
        # Supporte soit un chemin (str) soit un file-like (UploadedFile de Streamlit)
        sample = None
        delim = None
        decimal = "."

        def _read_sample(f):
            # lire un échantillon pour détecter le séparateur
            try:
                pos = f.tell()
            except Exception:
                pos = None
            sample_bytes = f.read(4096)
            try:
                if pos is not None:
                    f.seek(pos)
            except Exception:
                pass
            return sample_bytes

        try:
            # obtenir un objet file-like et un échantillon (bytes)
            if isinstance(fichier, str):
                with open(fichier, "rb") as fh:
                    sample = _read_sample(fh)
                fh2 = open(fichier, "rb")
                file_like = fh2
            else:
                # streamlit UploadedFile fournit .getvalue() et file-like methods
                try:
                    # si c'est un buffer (BytesIO)
                    file_like = fichier
                    sample = _read_sample(file_like)
                except Exception:
                    # fallback: lire les bytes
                    b = fichier.getvalue()
                    sample = b[:4096]
                    file_like = io.BytesIO(b)

            text_sample = sample.decode("utf-8", errors="replace") if isinstance(sample, (bytes, bytearray)) else str(sample)

            # essayer csv.Sniffer pour détecter le délimiteur
            try:
                dialect = csv.Sniffer().sniff(text_sample, delimiters=[",", "\t", ";", "|"])
                delim = dialect.delimiter
            except Exception:
                # fallback: compter les délimiteurs communs
                counts = {d: text_sample.count(d) for d in [";", ",", "\t", "|"]}
                delim = max(counts, key=counts.get)

            # détecter le séparateur décimal — si on a des nombres avec des virgules
            # mais que le délimiteur n'est pas la virgule, on utilisera decimal=','
            if re.search(r"\d+,\d+", text_sample) and delim != ",":
                decimal = ","

            # maintenant lire avec pandas
            # s'assurer de remettre le pointeur au début
            try:
                file_like.seek(0)
            except Exception:
                pass

            # pandas accepte les objets file-like (bytes) mais attend du texte; utiliser engine python
            # pour la détection correcte du séparateur quand nécessaire
            self.data = pd.read_csv(
                file_like,
                sep=delim,
                decimal=decimal,
                engine="python",
            )

            # tentative de parsing automatique de la première colonne en datetime si son nom est Date
            if "Date" in self.data.columns:
                try:
                    self.data["Date"] = pd.to_datetime(self.data["Date"], dayfirst=True, errors="coerce")
                    # si conversion OK, définir en index
                    if self.data["Date"].notna().any():
                        self.data.set_index("Date", inplace=True)
                except Exception:
                    pass

            # fermer le fichier si on l'a ouvert nous-mêmes
            if isinstance(fichier, str):
                fh2.close()

        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")
            self.data = None

    def load_data_from_dict(self, data_dict):
        """Charge les données depuis un dictionnaire"""
        try:
            self.data = pd.DataFrame(data_dict)
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
        from systeme_sauvegarde import load
        """Affiche la page avec les données et le drag and drop"""
        st.title(self.titre)

        # Zone de drag and drop pour importer un fichier CSV
        st.subheader("Importer un fichier CSV")
        uploaded_file = st.file_uploader(
            "Glissez-déposez votre fichier CSV ici ou cliquez pour parcourir",
            type="csv",
            label_visibility="collapsed",
        )
        st.subheader("Importer une sauvegarde JSON")
        uploaded_file_json = st.file_uploader(
            "Glissez-déposez votre fichier de sauvegarde ici ou cliquez pour parcourir",
            type="json",
            label_visibility="collapsed",
        )
        # Traiter la sauvegarde JSON
        if uploaded_file_json is not None:
            sauvegarde_str = uploaded_file_json.getvalue().decode("utf-8")
            # Récupérer (ou initialiser) les instances dans la session
            graphiques_inst = st.session_state.get("graphiques")
            donnees_inst = st.session_state.get("données", self)
            if graphiques_inst is None:
                from page_graphique_V3 import Graphiques

                graphiques_inst = Graphiques()
                st.session_state.graphiques = graphiques_inst
            # Assurer que la page de données en session existe
            st.session_state.données = donnees_inst
            # Charger la sauvegarde et mettre à jour les instances
            graphiques_inst, donnees_inst = load(
                sauvegarde_str, graphiques_inst, donnees_inst
            )
            st.session_state.graphiques = graphiques_inst
            st.session_state.données = donnees_inst
            self.data = donnees_inst.data
        # Traiter le fichier uploadé
        if uploaded_file is not None:
            try:
                # Charger le fichier en utilisant la méthode robuste
                self.load_data(uploaded_file)
                st.session_state.données = self
                st.success("Fichier chargé avec succès!")
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier: {str(e)}")

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

        st.sidebar.subheader("Importer une sauvegarde")
        uploaded_file = st.sidebar.file_uploader(
            "Choisissez un fichier de sauvegarde", type=["json"]
        )
        if uploaded_file is not None:
            sauvegarde_str = uploaded_file.getvalue().decode("utf-8")
            # Utiliser les instances stockées dans la session si disponibles
            graphiques_inst = st.session_state.get("graphiques")
            donnees_inst = st.session_state.get("données", self)
            if graphiques_inst is None:
                from page_graphique_V3 import Graphiques

                graphiques_inst = Graphiques()
            graphiques_inst, donnees_inst = load(
                sauvegarde_str, graphiques_inst, donnees_inst
            )
            st.session_state.graphiques = graphiques_inst
            st.session_state.données = donnees_inst
            self.data = donnees_inst.data
        else:
            pass
