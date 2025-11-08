import streamlit as st
from typing import List
import pandas as pd


class Graphiques:
    def __init__(self) -> None:
        self.datas = {}
        self.lines: List[List[Area]] = []

    def render(self):
        st.subheader("Deux premiers graphiques")
        for line in self.lines:
            columns = st.columns([1 / len(self.lines) for i in range(len(self.lines))])
            for i in range(len(line)):
                with columns[i]:
                    line[i].render()

    def set_datas(self, area_name: str, data: pd.DataFrame):
        self.datas[area_name] = data

    def add_column(self, line: int, area_name: str, type, data: pd.DataFrame | None = None, show_name: bool = True):
        self.lines[line].append(Area(area_name, type, data, show_name))


class Area:
    BARCHART = 1
    LINECHART = 2
    SCATTER = 4

    def __init__(self, area_name, type, data: pd.DataFrame | None = None, show_name: bool = True) -> None:
        self.data = data
        self.show_name = show_name
        self.area_name = area_name
        self.content_type = type
        return

    def render(self):
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
