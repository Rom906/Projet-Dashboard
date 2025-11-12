import streamlit as st
from typing import List
import pandas as pd


class Graphiques:
    def __init__(self) -> None:
        self.datas = {}
        self.lines: List[Ligne] = []

    def render(self) -> None:
        st.subheader("Deux premiers graphiques")
        for line in self.lines:
            line.render()

    def set_datas(self, line_title: str, area_name: str, data: pd.DataFrame) -> None:
        for line in self.lines:
            if line.title == line_title:
                line.set_data(area_name, data)

    def add_area(self, line: int, area_name: str, type, data: pd.DataFrame | None = None, show_name: bool = True) -> None:
        self.lines[line].add_area(area_name, type, data)

    def add_line(self, line_name: str, show_name: bool = True) -> None:
        self.lines.append(Ligne(len(self.lines), line_name, show_name))

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
            lines_names = line.get_areas_names
            for area_name in lines_names:  # type: ignore
                names.append(area_name)
        return names

    def get_line_index(self, line_title: str) -> int | None:
        for i in range(len(self.lines)):
            if self.lines[i].title == line_title:
                return i
        return None


class Ligne:
    def __init__(self, index: int, title: str, show_title: bool = True) -> None:
        self.title = title
        self.index = index
        self.show_title = show_title
        self.areas: List[Area] = []

    def render(self) -> None:
        columns = st.columns([1 / len(self.areas) for i in range(len(self.areas))])
        for i in range(len(self.areas)):
            with columns[i]:
                self.areas[i].render()

    def add_area(self, area_name: str, type, data: pd.DataFrame | None = None, show_name: bool = True) -> None:
        self.areas.append(Area(area_name, type, data, show_name))

    def get_areas_names(self) -> List[str]:
        names = []
        for area in self.areas:
            names.append(area.area_name)
        return names

    def set_data(self, area_name: str, data: pd.DataFrame) -> None:
        for area in self.areas:
            if area.area_name == area_name:
                area.set_data(data)
                return


class Area:
    BARCHART = 1
    LINECHART = 2
    SCATTER = 3

    def __init__(self, area_name, graphic_type: str | int, data: pd.DataFrame | None = None, show_name: bool = True) -> None:
        self.data = data
        self.show_name = show_name
        self.area_name = area_name
        if type(graphic_type) is str:
            self.content_type = self.convert_type(graphic_type)
        elif type(graphic_type) is int:
            self.content_type = graphic_type
        else:
            raise TypeError("mauvais type de type de graphique entré")
        return

    def render(self) -> None:
        if self.content_type == self.BARCHART:
            if self.show_name:
                st.subheader(self.area_name)
            st.bar_chart(self.data)
        elif self.content_type == self.LINECHART:
            if self.show_name:
                st.subheader(self.area_name)
            st.line_chart(self.data)
        elif self.content_type == self.SCATTER:
            if self.show_name:
                st.subheader(self.area_name)
            st.scatter_chart(self.data)

    def set_data(self, data: pd.DataFrame) -> None:
        self.data = data

    # à mettre à jour à chaque ajout
    @staticmethod
    def convert_type(type: str) -> int:
        if type == "Histograme":
            return 1
        elif type == "Graphique normal":
            return 2
        elif type == "Nuage de points":
            return 3
        else:
            raise TypeError("wrong type for graphic")

    @staticmethod
    def get_types() -> List[str]:
        return ["Histograme", "Graphique normal", "Nuage de points"]
