import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt
%matplotlib inline


prices = pd.read_csv("prices.csv", index_col=1, parse_dates=True)
invest_info = pd.read_csv("invest_info.csv", index_col=0)
curves = pd.read_csv("curves.csv", index_col=1, parse_dates=True)
curves_cons = curves.sum(1)

# Interface Streamlit
tab1, tab2, tab3 = st.tabs(["Resultado consolidado", "Tabela de preços", "Tabela de cotas"])

with tab1:
    st.title("Evolução do patrimônio")
    st.subheader("Consolidado")
    consolidado = px.bar(curves_cons, x=eixo_x, y="AUM", color_discrete_sequence=["steelblue"])
    st.plotly_chart(consolidado, use_container_width=True, config={"staticPlot": True})
    st.subheader("Por classe")
    classe = px.bar(curves, x=eixo_x, y="AUM", color_discrete_sequence=["steelblue"])
    st.plotly_chart(classe, use_container_width=True, config={"staticPlot": True})
    st.subheader("Por fundo")
    fundo = px.bar(curves, x=eixo_x, y="AUM", color_discrete_sequence=["steelblue"])
    st.plotly_chart(fundo, use_container_width=True, config={"staticPlot": True})

with tab2:
    st.title("Informações gerais")
    #st.subheader("Gráfico de Vitórias")
    st.dataframe(invest_info)

with tab3:
    st.title("Tabela de preço")
    #st.subheader("Gráfico de Vitórias")
    st.dataframe(prices.sort_index(ascending=False))
