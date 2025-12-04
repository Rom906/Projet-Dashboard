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

            text_sample = (
                sample.decode("utf-8", errors="replace")
                if isinstance(sample, (bytes, bytearray))
                else str(sample)
            )

            # essayer csv.Sniffer pour détecter le délimiteur
            try:
                dialect = csv.Sniffer().sniff(
                    text_sample, delimiters=[",", "\t", ";", "|"]
                )
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
                    self.data["Date"] = pd.to_datetime(
                        self.data["Date"], dayfirst=True, errors="coerce"
                    )
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

    def get_lines(self, lines_indices: List[int]):
        """Récupère des lignes spécifiques du DataFrame à partir de leurs indices

        Args:
            lines_indices (List[int]): Liste des indices des lignes à récupérer

        Returns:
            pd.DataFrame: DataFrame contenant uniquement les lignes demandées
        """
        if self.data is not None:
            return self.data.iloc[lines_indices]
        return None

    def add_row(self, row_data: dict):
        """Ajoute une nouvelle ligne au DataFrame

        Args:
            row_data (dict): Dictionnaire contenant les données de la nouvelle ligne
                            Les clés doivent correspondre aux colonnes existantes
        """
        if self.data is None:
            # Si pas de données, créer un nouveau DataFrame à partir du dictionnaire
            self.data = pd.DataFrame([row_data])
        else:
            # Ajouter une nouvelle ligne
            new_row = pd.DataFrame([row_data])
            self.data = pd.concat([self.data, new_row], ignore_index=True)
        # Force Streamlit à reconnaître le changement
        self.data = self.data.copy()
        # Sauvegarder en session state
        self._save_to_session_state()

    def edit_row(self, row_index: int, row_data: dict):
        """Modifie une ligne existante du DataFrame

        Args:
            row_index (int): Index de la ligne à modifier
            row_data (dict): Dictionnaire contenant les données mises à jour
        """
        if self.data is not None and row_index < len(self.data):
            for col, value in row_data.items():
                if col in self.data.columns:
                    self.data.at[row_index, col] = value
        # Force Streamlit à reconnaître le changement
        self.data = self.data.copy()
        # Sauvegarder en session state
        self._save_to_session_state()

    def delete_row(self, row_index: int):
        """Supprime une ligne du DataFrame

        Args:
            row_index (int): Index de la ligne à supprimer
        """
        if self.data is not None and row_index < len(self.data):
            self.data = self.data.drop(row_index).reset_index(drop=True)
        # Force Streamlit à reconnaître le changement
        self.data = self.data.copy()
        # Sauvegarder en session state
        self._save_to_session_state()

    def _save_to_session_state(self):
        """Sauvegarde les données actuelles en JSON dans la session state pour persistance"""
        if self.data is not None:
            try:
                import json

                # Créer un dictionnaire sérializable avec gestion complète des types
                data_dict = {}
                for col in self.data.columns:
                    col_data = []
                    for val in self.data[col]:
                        # Gérer les valeurs manquantes
                        if val is None or (isinstance(val, float) and pd.isna(val)):
                            col_data.append(None)
                        # Gérer les types sérializables
                        elif isinstance(val, (int, float, str, bool)):
                            col_data.append(val)
                        # Gérer numpy types
                        elif hasattr(val, "item"):  # numpy types
                            col_data.append(val.item())
                        # Fallback: convertir en string
                        else:
                            col_data.append(str(val))
                    data_dict[col] = col_data

                # Sauvegarder en JSON en session state (JSON valide avec null au lieu de NaN)
                json_str = json.dumps(data_dict, ensure_ascii=False)
                st.session_state["données_backup_json"] = json_str
            except Exception as e:
                import traceback

                st.write(f"❌ Erreur sauvegarde JSON: {e}")

    def _load_from_session_state(self):
        """Recharge les données depuis le JSON sauvegardé en session state"""
        if (
            "données_backup_json" in st.session_state
            and st.session_state["données_backup_json"]
        ):
            try:
                import json

                json_str = st.session_state["données_backup_json"]
                if not json_str or json_str == "":
                    return

                data_dict = json.loads(json_str)
                new_data = pd.DataFrame(data_dict)

                if not new_data.empty:
                    self.data = new_data
            except json.JSONDecodeError as e:
                import traceback

                st.write(f"❌ Erreur JSON invalide lors du chargement")
                st.write(f"Erreur: {e}")
            except Exception as e:
                import traceback

                st.write(f"❌ Erreur lors du chargement des données")
                st.write(f"Erreur: {e}")

    def add_column_from_operation(
        self, column_name: str, operation: str, column_operand: str
    ):
        """Crée une nouvelle colonne calculée à partir d'une opération statistique

        Args:
            column_name (str): Nom de la nouvelle colonne
            operation (str): Type d'opération ('somme', 'moyenne', 'médiane', 'écart_type', 'variance')
            column_operand (str): Colonne source sur laquelle appliquer l'opération
                                  (ignorée pour les opérations simples, utilisée pour les calculs)
        """
        if self.data is None:
            st.error("Aucune donnée disponible")
            return False

        try:
            if operation == "somme":
                self.data[column_name] = self.data[column_operand].sum()
            elif operation == "moyenne":
                self.data[column_name] = self.data[column_operand].mean()
            elif operation == "médiane":
                self.data[column_name] = self.data[column_operand].median()
            elif operation == "écart_type":
                self.data[column_name] = self.data[column_operand].std()
            elif operation == "variance":
                self.data[column_name] = self.data[column_operand].var()
            else:
                st.error(f"Opération inconnue: {operation}")
                return False
            return True
        except Exception as e:
            st.error(f"Erreur lors du calcul: {str(e)}")
            return False

    def get_sum(self, column_name: str) -> float:
        """Retourne la somme d'une colonne"""
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name].sum()
        return None

    def get_mean(self, column_name: str) -> float:
        """Retourne la moyenne d'une colonne"""
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name].mean()
        return None

    def get_median(self, column_name: str) -> float:
        """Retourne la médiane d'une colonne"""
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name].median()
        return None

    def get_std(self, column_name: str) -> float:
        """Retourne l'écart type d'une colonne"""
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name].std()
        return None

    def get_variance(self, column_name: str) -> float:
        """Retourne la variance d'une colonne"""
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name].var()
        return None

    def afficher_page(self):
        from systeme_sauvegarde import load

        """Affiche la page avec les données et le drag and drop"""
        # ÉTAPE CRITIQUE : Recharger les données depuis le backup JSON en session state
        # Ceci garantit que les modifications précédentes persisteront
        self._load_from_session_state()

        # SYNCHRONISER SELF avec ST.SESSION_STATE
        st.session_state["données"] = self

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
            # IMPORTANT: Sauvegarder les données chargées en JSON dans la session state
            # Ceci crée le backup JSON à partir de la sauvegarde complète chargée
            if self.data is not None:
                try:
                    import json

                    data_dict = {}
                    for col in self.data.columns:
                        col_data = []
                        for val in self.data[col]:
                            if pd.isna(val):
                                col_data.append(None)
                            elif isinstance(val, (int, float, str, bool)):
                                col_data.append(val)
                            elif hasattr(val, "item"):  # numpy types
                                col_data.append(val.item())
                            else:
                                col_data.append(str(val))
                        data_dict[col] = col_data
                    st.session_state["données_backup_json"] = json.dumps(
                        data_dict, ensure_ascii=False
                    )
                    st.write(f"✅ Sauvegarde importée: {len(data_dict)} colonnes")
                except Exception as e:
                    st.write(f"❌ Erreur création backup JSON: {e}")
        # Traiter le fichier uploadé
        if uploaded_file is not None:
            # Créer une clé unique pour ce fichier pour tracker s'il a déjà été chargé
            file_key = f"loaded_file_{uploaded_file.name}_{uploaded_file.size}"

            # Ne charger que si ce fichier n'a pas déjà été traité
            if file_key not in st.session_state or not st.session_state[file_key]:
                try:
                    # Charger le fichier en utilisant la méthode robuste
                    self.load_data(uploaded_file)
                    # Sauvegarder immédiatement en session state
                    self._save_to_session_state()
                    st.session_state[file_key] = True  # Marquer comme chargé
                    st.write(
                        f"✅ CSV importé: {len(self.data)} lignes, {len(self.data.columns)} colonnes"
                    )
                except Exception as e:
                    st.write(f"❌ Erreur lors du chargement du fichier: {str(e)}")

        st.divider()

        # Section Créer ou modifier des données
        st.subheader("Ajouter une nouvelle ligne")

        # Initialiser le compteur de resets si nécessaire
        if "add_row_counter" not in st.session_state:
            st.session_state.add_row_counter = 0

        if self.data is None:
            st.info(
                "Aucune donnée. Veuillez d'abord importer un fichier CSV ou créer des données."
            )
        else:
            colonnes = self.data.columns.to_list()
            col_inputs = st.columns(len(colonnes))
            row_data = {}

            # Utiliser le compteur dans les clés pour forcer le reset après chaque ajout
            for idx, col in enumerate(colonnes):
                with col_inputs[idx]:
                    row_data[col] = st.text_input(
                        f"{col}",
                        key=f"new_row_{col}_{st.session_state.add_row_counter}",
                    )

            if st.button("➕ Ajouter la ligne"):
                try:
                    # Tenter de convertir les valeurs au type approprié
                    converted_data = {}
                    for col, val in row_data.items():
                        if val == "":
                            converted_data[col] = None
                        else:
                            # Essayer de convertir en nombre si possible
                            try:
                                converted_data[col] = float(val)
                            except ValueError:
                                # Garder comme string si ce n'est pas un nombre
                                converted_data[col] = val

                    self.add_row(converted_data)
                    st.session_state.add_row_counter += 1
                    st.write("✅ Ligne ajoutée avec succès!")
                    try:
                        st.rerun()  # Forcer le rerun pour recalculer l'affichage du tableau
                    except AttributeError:
                        # Fallback pour les versions anciennes de Streamlit
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'ajout de la ligne: {str(e)}")
                    import traceback

                    st.error(traceback.format_exc())

        st.divider()

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
            st.dataframe(self.data, width="stretch")

            # Ajouter des statistiques de base
            st.subheader("Statistiques descriptives")
            st.dataframe(self.data.describe(), width="stretch")

            # Section pour gérer les lignes
            st.subheader("Gérer les lignes")

            # Initialiser la session state pour l'action sélectionnée
            if "selected_action" not in st.session_state:
                st.session_state.selected_action = "Afficher"

            # Utiliser des boutons au lieu d'un radio pour éviter les reruns automatiques
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Afficher", use_container_width=True):
                    st.session_state.selected_action = "Afficher"
            with col2:
                if st.button("✏️ Modifier un élément", use_container_width=True):
                    st.session_state.selected_action = "Modifier un élément"
            with col3:
                if st.button("🗑️ Supprimer une ligne", use_container_width=True):
                    st.session_state.selected_action = "Supprimer une ligne"

            # Initialiser les compteurs de resets si nécessaire
            if "edit_row_counter" not in st.session_state:
                st.session_state.edit_row_counter = 0
            if "delete_row_counter" not in st.session_state:
                st.session_state.delete_row_counter = 0

            action = st.session_state.selected_action

            if action == "Afficher":
                st.write("**Sélectionner des lignes à afficher**")

                # Option 1: Sélection par plage
                st.write("**Option 1 : Sélectionner une plage**")
                col1, col2 = st.columns(2)
                with col1:
                    start_index = st.number_input(
                        "Indice de début",
                        min_value=0,
                        max_value=len(self.data) - 1,
                        value=0,
                        key="start_range",
                    )
                with col2:
                    end_index = st.number_input(
                        "Indice de fin (inclus)",
                        min_value=start_index,
                        max_value=len(self.data) - 1,
                        value=min(start_index + 4, len(self.data) - 1),
                        key="end_range",
                    )

                if st.button("📊 Afficher la plage"):
                    selected_lines = self.get_lines(
                        list(range(start_index, end_index + 1))
                    )
                    st.dataframe(selected_lines, width="stretch")

                st.divider()

                # Option 2: Sélection individuelle
                st.write("**Option 2 : Sélectionner des lignes individuelles**")
                indices = st.multiselect(
                    "Choisissez les indices des lignes à afficher",
                    range(len(self.data)),
                    key="select_indices",
                )
                if indices:
                    selected_lines = self.get_lines(sorted(indices))
                    st.dataframe(selected_lines, width="stretch")

            elif action == "Modifier un élément":
                col1, col2 = st.columns(2)

                with col1:
                    row_index = st.number_input(
                        "Numéro de la ligne",
                        min_value=0,
                        max_value=len(self.data) - 1,
                        value=0,
                        key=f"edit_row_index_{st.session_state.edit_row_counter}",
                    )

                with col2:
                    column_name = st.selectbox(
                        "Colonne à modifier",
                        self.data.columns.to_list(),
                        key=f"edit_column_{st.session_state.edit_row_counter}",
                    )

                # Afficher la ligne actuelle
                st.write("**Ligne actuelle:**")
                st.dataframe(self.data.iloc[row_index : row_index + 1], width="stretch")

                # Afficher la valeur actuelle
                current_value = self.data.at[row_index, column_name]
                st.info(f"Valeur actuelle de **{column_name}**: `{current_value}`")

                # Permettre de modifier juste cet élément
                new_value = st.text_input(
                    f"Nouvelle valeur pour {column_name}",
                    value=str(current_value),
                    key=f"edit_value_{st.session_state.edit_row_counter}",
                )

                if st.button("✏️ Modifier cet élément"):
                    try:
                        # Essayer de convertir en nombre si possible
                        try:
                            converted_value = float(new_value)
                        except ValueError:
                            converted_value = new_value

                        self.edit_row(row_index, {column_name: converted_value})
                        st.session_state.edit_row_counter += 1
                        st.success(f"✅ {column_name} modifié avec succès!")
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la modification: {str(e)}")
                        import traceback

                        st.error(traceback.format_exc())

            elif action == "Supprimer une ligne":
                row_index = st.number_input(
                    "Numéro de la ligne à supprimer",
                    min_value=0,
                    max_value=len(self.data) - 1,
                    value=0,
                    key=f"delete_row_index_{st.session_state.delete_row_counter}",
                )
                st.warning("Ligne à supprimer:")
                st.dataframe(self.data.iloc[row_index : row_index + 1], width="stretch")

                if st.button("🗑️ Supprimer cette ligne", type="secondary"):
                    try:
                        self.delete_row(row_index)
                        st.session_state.delete_row_counter += 1
                        st.success("✅ Ligne supprimée!")
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la suppression: {str(e)}")
                        import traceback

                        st.error(traceback.format_exc())
        else:
            st.info("Aucune donnée n'a été chargée. Veuillez importer un fichier CSV.")

        # Afficher le uploader de sauvegarde dans la sidebar uniquement
        # si on n'est pas déjà sur la page "Données" (demande utilisateur).
        current_page = st.session_state.get("page", "")
        if current_page != "Données":
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
            # quand on est sur la page 'Données', on n'affiche pas l'uploader
            pass
