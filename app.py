import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
prices = pd.read_csv("prices.csv", index_col=0, parse_dates=True)
invest_info = pd.read_csv("invest_info.csv", index_col=0)
curves = pd.read_csv("curves.csv", index_col=0, parse_dates=True)
curves_cons = curves.sum(axis=1).reset_index()  # Reset index para compatibilidade com Plotly

# Interface Streamlit
tab1, tab2, tab3 = st.tabs(["Resultado consolidado", "Tabela de preços", "Tabela de cotas"])

with tab1:
    st.title("Evolução do patrimônio")
    st.subheader("Consolidado")
    consolidado = px.bar(curves_cons, x="index", y=0, color_discrete_sequence=["steelblue"], labels={"index": "Data", 0: "AUM"})
    st.plotly_chart(consolidado, use_container_width=True)

    st.subheader("Por classe")
    if not curves.empty:
        classe = px.bar(curves.reset_index(), x="index", y="AUM", color_discrete_sequence=["steelblue"])
        st.plotly_chart(classe, use_container_width=True)

    st.subheader("Por fundo")
    if not curves.empty:
        fundo = px.bar(curves.reset_index(), x="index", y="AUM", color_discrete_sequence=["steelblue"])
        st.plotly_chart(fundo, use_container_width=True)

with tab2:
    st.title("Informações gerais")
    st.dataframe(invest_info)

with tab3:
    st.title("Tabela de preço")
    st.dataframe(prices.sort_index(ascending=False))
