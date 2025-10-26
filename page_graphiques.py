import streamlit as st
from typing import Tuple
import pandas as pd


class Graphiques:
    def __init__(self, datas: Tuple[pd.DataFrame, pd.DataFrame]) -> None:
        self.datas = datas

    def render(self):
        st.subheader("Deux premiers graphiques")
        columns = st.columns([0.5, 0.5])
        for column, data in zip(columns, self.datas):
            with column:
                if data is not None and not data.empty:
                    st.bar_chart(data)
        st.subheader("Deux autres graphiques dont on choisit le contenu")
