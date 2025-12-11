import streamlit as st
from typing import List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm, chi2


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


class Graphiques:
    def __init__(self) -> None:
        self.datas = {}
        self.lines: List[Ligne] = []

    def render(self) -> None:
        for line in self.lines:
            line.render()

    def set_datas(self, line_title: str, area_name: str, data: pd.DataFrame) -> None:
        for line in self.lines:
            if line.title == line_title:
                line.set_data(area_name, data)

    def set_area_abscisse_column(
        self, line_title: str, area_name: str, abcsisse_column_name: str
    ):
        for line in self.lines:
            if line.title == line_title:
                line.set_area_abscisse_column(area_name, abcsisse_column_name)

    def add_area(
        self,
        line: int,
        area_name: str,
        type,
        data: pd.DataFrame | None = None,
        show_name: bool = True,
    ) -> None:
        self.lines[line].add_area(area_name, type, data)

    def delete_area(self, line_title: str, area_name: str):
        for line in self.lines:
            if line.title == line_title:
                line.delete_area(area_name)
                return

    def add_line(self, line_name: str, show_name: bool = True) -> None:
        self.lines.append(Ligne(len(self.lines), line_name, show_name))

    def delete_line(self, line_title: str):
        for i in range(len(self.lines)):
            if self.lines[i].title == line_title:
                self.lines.pop(i)
                return

    def get_lines_count(self) -> int:
        return len(self.lines)

    def get_lines_titles(self) -> List[str]:
        titles = []
        for line in self.lines:
            titles.append(line.title)
        return titles

    def get_areas_names(self) -> List[str]:
        names = []
        for line in self.lines:
            lines_names = line.get_areas_names()
            for area_name in lines_names:  # type: ignore
                names.append(area_name)
        return names

    def get_area_ploted_columns(self, line_title: str, area_name: str) -> List[str]:
        for line in self.lines:
            if line.title == line_title:
                return line.get_area_plotted_columns(area_name)
        return []

    def get_area_abscisse_column_name(
        self, line_title: str, area_name: str
    ) -> str | None:
        for line in self.lines:
            if line.title == line_title:
                line.get_area_abscisse_column_name(area_name)
                return

    def get_line_areas_names(self, line_title: str) -> List[str]:
        for line in self.lines:
            if line.title == line_title:
                return line.get_areas_names()
        raise KeyError("Aucune ligne n'a ce nom")

    def get_line_index(self, line_title: str) -> int | None:
        for i in range(len(self.lines)):
            if self.lines[i].title == line_title:
                return i
        return None

    def render_area_sidebar_options(self, line_title: str, area_name: str):
        for line in self.lines:
            if line.title == line_title:
                line.render_area_sidebar_options(area_name)
                return


class Ligne:
    def __init__(self, index: int, title: str, show_title: bool = True) -> None:
        self.title = title
        self.index = index
        self.show_title = show_title
        self.areas: List[Area] = []

    def render(self) -> None:
        if self.show_title:
            st.markdown(f"# {self.title}")
        if self.areas == []:
            return
        with st.container():
            columns = st.columns([1 / len(self.areas) for i in range(len(self.areas))])
            for i in range(len(self.areas)):
                with columns[i]:
                    self.areas[i].render()

    def add_area(
        self,
        area_name: str,
        type,
        data: pd.DataFrame | None = None,
        show_name: bool = True,
    ) -> None:
        self.areas.append(Area(area_name, type, data, show_name))

    def delete_area(self, area_name: str):
        for i in range(len(self.areas)):
            if self.areas[i].area_name == area_name:
                self.areas.pop(i)
                return

    def get_areas_names(self) -> List[str]:
        names = []
        for area in self.areas:
            names.append(area.area_name)
        return names

    def get_area_plotted_columns(self, area_name: str) -> List[str]:
        for area in self.areas:
            if area.area_name == area_name:
                if area.data is not None:
                    area_data = area.data
                    return area_data.columns.to_list()
                else:
                    return []
        return []

    def get_area_abscisse_column_name(self, area_name: str) -> str | None:
        for area in self.areas:
            if area.area_name == area_name:
                return area.abscisse_column_name

    def set_data(self, area_name: str, data: pd.DataFrame) -> None:
        for area in self.areas:
            if area.area_name == area_name:
                area.set_data(data)
                return

    def set_area_abscisse_column(self, area_name: str, abscisse_column_name: str):
        for area in self.areas:
            if area.area_name == area_name:
                area.set_abscisse_column(abscisse_column_name)

    def render_area_sidebar_options(self, area_name):
        for area in self.areas:
            if area.area_name == area_name:
                area.render_sidebar_options()
                return


class Area:
    BARCHART = 1
    LINECHART = 2
    SCATTER = 3
    MARKDOWN = 4
    KHI2 = 5

    def __init__(
        self,
        area_name,
        graphic_type: str | int,
        data: pd.DataFrame | None = None,
        show_name: bool = True,
    ) -> None:
        self.data = data
        self.show_name = show_name
        self.area_name = area_name
        self.abscisse_column_name = None
        if data is not None and not data.empty:
            min_value = 0
            max_value = data.shape[0] - 1
            self.range = (min_value, max_value)
        else:
            self.range: Tuple = (None, None)

        if type(graphic_type) is str:
            self.content_type = self.convert_type(graphic_type)
        elif type(graphic_type) is int:
            self.content_type = graphic_type
        else:
            raise TypeError("mauvais type de type de graphique entré")

        if self.content_type == self.MARKDOWN:
            self.input_mode = True
            self.text = None

        if self.content_type == self.KHI2:
            self.theo = []
        return

    def render(self) -> None:
        if self.content_type == self.MARKDOWN:
            if self.show_name:
                st.subheader(self.area_name)
            self.render_markdown()
        if self.data is not None and not self.data.empty:
            if self.content_type == self.BARCHART:
                if self.show_name:
                    st.subheader(self.area_name)
                self.render_barchart()
            elif self.content_type == self.LINECHART:
                if self.show_name:
                    st.subheader(self.area_name)
                self.render_linechart()
            elif self.content_type == self.SCATTER:
                if self.show_name:
                    st.subheader(self.area_name)
                self.render_scatter()
            elif self.content_type == self.KHI2:
                if self.show_name:
                    st.subheader(self.area_name)
                self.render_khi2()

    def render_barchart(self):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots()
        data_frame = self.data.melt(var_name="nom_colonne", value_name="values")  # type: ignore
        data_frame_avec_comptage = (
            data_frame.groupby(["values", "nom_colonne"])
            .size()
            .reset_index(name="count")
        )
        data_frame_avec_comptage = data_frame_avec_comptage[
            (data_frame_avec_comptage["values"] >= self.range[0])
            & (data_frame_avec_comptage["values"] <= self.range[1])
        ]
        sns.barplot(
            data=data_frame_avec_comptage,
            x="values",
            y="count",
            hue="nom_colonne",
            ax=ax,
            dodge=True,
        )
        st.pyplot(fig)

    def render_linechart(self):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots()
        plotted_columns = self.data.columns.to_list()  # type: ignore
        if self.abscisse_column_name is not None:
            plotted_columns.remove(self.abscisse_column_name)
            data_frame = self.data.melt(id_vars=self.abscisse_column_name, value_vars=plotted_columns, var_name="nom_colonne", value_name="values")  # type: ignore
            data_frame = data_frame[
                (data_frame[self.abscisse_column_name] >= self.range[0])
                & (data_frame[self.abscisse_column_name] <= self.range[1])
            ]
            sns.lineplot(data=data_frame, x=self.abscisse_column_name, y="values", hue="nom_colonne", ax=ax)  # type: ignore
        else:
            for column in self.data.columns:  # type: ignore
                sns.lineplot(x=self.data.index, y=self.data[column], ax=ax)  # type: ignore
        st.pyplot(fig)

    def render_scatter(self):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots()
        if self.abscisse_column_name is not None:
            data_filtered = self.data[(self.data[self.abscisse_column_name] > self.range[0]) & (self.data[self.abscisse_column_name] < self.range[1])]  # type: ignore
        else:
            data_filtered = self.data.loc[self.range[0] : self.range[1]]  # type: ignore
        plotted_columns = self.data.columns.to_list()  # type: ignore
        if self.abscisse_column_name:
            plotted_columns.remove(self.abscisse_column_name)
            abscisse = data_filtered[self.abscisse_column_name]  # type: ignore
        else:
            abscisse = self.data.index  # type: ignore

        for column in plotted_columns:
            sns.scatterplot(x=abscisse, y=data_filtered[column])  # type: ignore
        st.pyplot(fig)

    def render_markdown(self):
        if self.input_mode:
            self.text = st.text_area(
                "Entrez votre texte en Markdown", value=self.text, height=400
            )
        else:
            st.markdown(self.text)

    def render_khi2(self):


        st.write("Effectifs observés")
        st.dataframe(self.data)
        st.write("Effectifs théoriques")
        st.dataframe(self.theo)

        accepte = True
        ddl = len(self.data.columns.to_list()) - 1
        for colonne in self.data.columns:
            x2calc = 0
            for i in range(len(self.data[colonne])):
                x2calc += (self.data[colonne].iloc[i] - self.theo[colonne].iloc[i]) ** 2 / (
                    self.theo[colonne].iloc[i]
                )
            x2crit = chi2.ppf(0.95, ddl)
            if x2calc > x2crit:
                accepte = False

        if accepte:
            st.markdown("# On ne peut pas réfuter la loi avec le test du khi2")
        else:
            st.markdown("# On peut réfuter la loi avec 5% de chance de se tromper")

    def set_data(self, data: pd.DataFrame) -> None:
        if data is not None and not data.empty:
            if self.data is None or self.data.empty:
                if self.content_type == self.BARCHART:
                    data_frame = data.melt(var_name="nom_colonne", value_name="values")
                    min_value = data_frame["values"].min()
                    max_value = data_frame["values"].max()
                    self.range = (min_value, max_value)
                else:
                    self.range = (0, data.shape[0] - 1)
            self.data = data
            if self.abscisse_column_name is None:
                return
            else:
                if self.abscisse_column_name in self.data.columns:
                    self.data.set_index(
                        self.abscisse_column_name, inplace=True, drop=False
                    )
                else:
                    self.abscisse_column_name = None

    def set_abscisse_column(self, abscisse_column_name: str | None):
        if self.data is not None and not self.data.empty:
            if abscisse_column_name is None:
                self.abscisse_column_name = None
                self.data.reset_index(drop=True, inplace=True)  # type: ignore
                self.data.index.name = "Index par défaut"  # type: ignore
                min_value = 0
                max_value = self.data.shape[0] - 1
                self.range = (min_value, max_value)
            elif abscisse_column_name in self.data.columns.to_list():  # type: ignore
                self.abscisse_column_name = abscisse_column_name  # type: ignore
                self.data.set_index(abscisse_column_name, drop=False, inplace=True)  # type: ignore
                min_value = self.data[abscisse_column_name].min()
                max_value = self.data[abscisse_column_name].max()
                self.range = (min_value, max_value)

    # à mettre à jour à chaque ajout
    @staticmethod
    def convert_type(type: str) -> int:
        if type == "Histogramme":
            return Area.BARCHART
        elif type == "Courbe":
            return Area.LINECHART
        elif type == "Nuage de points":
            return Area.SCATTER
        elif type == "Markdown":
            return Area.MARKDOWN
        elif type == "Khi2":
            return Area.KHI2
        else:
            raise KeyError("wrong type for graphic")

    @staticmethod
    def get_types() -> List[str]:
        return ["Histogramme", "Courbe", "Nuage de points", "Markdown", "Khi2"]

    def render_sidebar_options(self):
        if self.content_type == Area.BARCHART:
            self.render_sidebar_options_barchart()
        elif self.content_type == Area.LINECHART:
            self.render_sidebar_options_linechart()
        elif self.content_type == Area.SCATTER:
            self.render_sidebar_options_scatter()
        elif self.content_type == Area.MARKDOWN:
            self.render_sidebar_options_markdown()
        elif self.content_type == Area.KHI2:
            self.render_sidebar_options_khi2()

    def render_sidebar_options_barchart(self):
        if (
            st.session_state.données.data is not None
            and len(st.session_state.données.data.columns) > 0
        ):
            st.subheader("Paramètres du graphique")
            st.subheader("Choix des données")
            colonnes_données = st.session_state.données.data.columns.to_list()  # type: ignore
            colonnes_affichées = st.multiselect(
                "Choississez les colonnes utilisées dans le graphique",
                colonnes_données,
                key="colonnes_affichées_default",
            )
            if colonnes_affichées:
                données_affichées = st.session_state.données.get_columns(
                    colonnes_affichées
                )
                self.set_data(données_affichées)  # type: ignore
                self.render_sidebar_abscisse_interval_choose()
        else:
            st.warning(
                "Aucune donnée disponible. Veuillez d'abord importer ou créer des données sur la page 'Données'."
            )

    def render_sidebar_options_linechart(self):
        if (
            st.session_state.données.data is not None
            and len(st.session_state.données.data.columns) > 0
        ):
            st.subheader("Paramètres du graphique")
            st.subheader("Choix des données")
            colonnes_données = st.session_state.données.data.columns.to_list()  # type: ignore
            colonnes_affichées = st.multiselect(
                "Choississez les colonnes utilisées dans le graphique",
                colonnes_données,
                key="colonnes_affichées_default",
            )
            if colonnes_affichées:
                données_affichées = st.session_state.données.get_columns(
                    colonnes_affichées
                )
                self.set_data(données_affichées)  # type: ignore

                st.subheader("Choix de l'axe d'abcisse")
                if self.abscisse_column_name is not None:
                    colonnes_affichées.remove(self.abscisse_column_name)
                    nouvelle_abscisse = st.selectbox(
                        "Séléctionnez la colonne à mettre en axe des abscisses",
                        [self.abscisse_column_name]
                        + ["Index par défaut"]
                        + colonnes_affichées,
                    )
                else:
                    nouvelle_abscisse = st.selectbox(
                        "Séléctionnez la colonne à mettre en axe des abscisses",
                        ["Index par défaut"] + colonnes_affichées,
                    )
                if nouvelle_abscisse != st.session_state.colonne_abscisse:
                    if nouvelle_abscisse != "Index par défaut":
                        self.set_abscisse_column(nouvelle_abscisse)
                        st.session_state.colonne_abscisse = nouvelle_abscisse
                    else:
                        self.set_abscisse_column(None)
                        st.session_state.colonne_abscisse = "Index par défaut"
                    safe_rerun()
                self.render_sidebar_abscisse_interval_choose()
        else:
            st.warning(
                "Aucune donnée disponible. Veuillez d'abord importer ou créer des données sur la page 'Données'."
            )

    def render_sidebar_options_scatter(self):
        if (
            st.session_state.données.data is not None
            and len(st.session_state.données.data.columns) > 0
        ):
            st.subheader("Paramètres du graphique")
            st.subheader("Choix des données")
            colonnes_données = st.session_state.données.data.columns.to_list()  # type: ignore
            colonnes_affichées = st.multiselect(
                "Choississez les colonnes utilisées dans le graphique",
                colonnes_données,
                key="colonnes_affichées_default",
            )
            if colonnes_affichées:
                données_affichées = st.session_state.données.get_columns(
                    colonnes_affichées
                )
                self.set_data(données_affichées)  # type: ignore

                st.subheader("Choix de l'axe d'abcisse")
                if self.abscisse_column_name is not None:
                    colonnes_affichées.remove(self.abscisse_column_name)
                    nouvelle_abscisse = st.selectbox(
                        "Séléctionnez la colonne à mettre en axe des abscisses",
                        [self.abscisse_column_name]
                        + ["Index par défaut"]
                        + colonnes_affichées,
                    )
                else:
                    nouvelle_abscisse = st.selectbox(
                        "Séléctionnez la colonne à mettre en axe des abscisses",
                        ["Index par défaut"] + colonnes_affichées,
                    )
                if nouvelle_abscisse != st.session_state.colonne_abscisse:
                    if nouvelle_abscisse != "Index par défaut":
                        self.set_abscisse_column(nouvelle_abscisse)
                        st.session_state.colonne_abscisse = nouvelle_abscisse
                    else:
                        self.set_abscisse_column(None)
                        st.session_state.colonne_abscisse = "Index par défaut"
                    safe_rerun()
                self.render_sidebar_abscisse_interval_choose()
        else:
            st.warning(
                "Aucune donnée disponible. Veuillez d'abord importer ou créer des données sur la page 'Données'."
            )

    def render_sidebar_options_markdown(self):
        if self.input_mode:
            label = "Arrêter de modifier"
        else:
            label = "Modifier le texte"
        if st.button(label):
            self.input_mode = not self.input_mode

    def render_sidebar_abscisse_interval_choose(self):
        if self.data is not None and not self.data.empty:
            if self.content_type == self.BARCHART:
                data_frame = self.data.melt(var_name="nom_colonne", value_name="values")
                min_value = data_frame["values"].min()
                max_value = data_frame["values"].max()
            elif self.range != (None, None):
                min_value = self.range[0]
                max_value = self.range[1]
            elif self.abscisse_column_name is None:
                min_value = 0
                max_value = self.data.shape[0] - 1
            else:
                min_value = self.data[self.abscisse_column_name].min()
                max_value = self.data[self.abscisse_column_name].max()
            self.range = st.slider(
                "Choisissez l'intervalle des données",
                min_value,
                max_value,
                (min_value, max_value),
            )

    def render_sidebar_options_khi2(self):
        if (
            st.session_state.données.data is not None
            and len(st.session_state.données.data.columns) > 0
        ):
            st.subheader("Choix des données")
            colonnes_données = st.session_state.données.data.columns.to_list()
            colonnes_affichées = st.multiselect(
                "Choississez les colonnes utilisées dans le test",
                colonnes_données,
                key="colonnes_affichées_khi2",
            )
            if colonnes_affichées:
                données_affichées = st.session_state.données.get_columns(
                    colonnes_affichées
                )
                self.set_data(données_affichées)

                # total par colonne (somme des effectifs observés)
                col_totals = self.data.sum(axis=0)

                st.subheader("Choix de la loi à tester : ")
                type_loi = st.selectbox(
                    "Loi théorique",
                    ["Équirépartition", "Loi normale"],
                )

                # index = modalités / classes (par exemple 0,1,2,... ou centres de classes)
                x = self.data.index.to_numpy()
                n_modalites = len(x)

                self.theo = pd.DataFrame(
                    index=self.data.index, columns=self.data.columns, dtype=float
                )

                if type_loi == "Équirépartition":
                    # même probabilité pour chaque modalité
                    # donc effectif théorique = total_colonne / n_modalites
                    for col in self.data.columns:
                        self.theo[col] = col_totals[col] / n_modalites

                elif type_loi == "Loi normale":
                # concaténer toutes les valeurs pour estimer mu et sigma (ou les demander)
                    toutes_valeurs = pd.concat([self.data[c] for c in self.data.columns])
                    x_all = toutes_valeurs.to_numpy(dtype=float)

                    mu = st.number_input(
                        "Valeur de l'espérance (μ) : ",
                        value=float(np.mean(x_all)),
                        key="mu_khi2",
                    )
                    sigma = st.number_input(
                        "Valeur de l'écart-type (σ) : ",
                        value=float(np.std(x_all, ddof=1)),
                        key="sigma_khi2",
                    )

                    obs_dict = {}
                    theo_dict = {}

                    for col in self.data.columns:
                        # effectifs observés = nombre de lignes qui ont la même valeur
                        obs_counts = self.data[col].value_counts().sort_index()
                        x = obs_counts.index.to_numpy(dtype=float)
                        total = obs_counts.sum()

                        dens = norm.pdf(x, loc=mu, scale=sigma)
                        p = dens / dens.sum()
                        theo_counts = p * total

                        obs_dict[col] = obs_counts
                        theo_dict[col] = pd.Series(theo_counts, index=obs_counts.index)

                    # union des valeurs possibles pour toutes les colonnes
                    index_union = sorted(set().union(*[s.index for s in obs_dict.values()]))
                    obs_df = pd.DataFrame(index=index_union)
                    theo_df = pd.DataFrame(index=index_union)

                    for col in self.data.columns:
                        obs_df[col] = obs_dict[col].reindex(index_union, fill_value=0.0)
                        theo_df[col] = theo_dict[col].reindex(index_union, fill_value=0.0)

                    # ICI seulement on remplace self.data et self.theo
                    self.data = obs_df    # effectifs observés par valeur
                    self.theo = theo_df   # effectifs théoriques par valeur

                st.write("Effectifs observés pour le test :")
                st.dataframe(self.data)
                st.write("Effectifs théoriques pour le test :")
                st.dataframe(self.theo)

        else:
            st.warning(
                "Aucune donnée disponible. Veuillez d'abord importer ou créer des données sur la page 'Données'."
            )
