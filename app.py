import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Carregar os dados
prices = pd.read_csv("prices.csv", index_col=0, parse_dates=True)
invest_info = pd.read_csv("invest_info.csv", index_col=0)
curves = pd.read_csv("curves.csv", index_col=0, parse_dates=True)

# Preprocessamento
curves = curves.replace(0, np.nan).dropna(how='all').round(0)
curves_cons = curves.sum(axis=1).astype(int).reset_index()
curves_cons.columns = ['Date', 'AUM']

# Interface Streamlit
tab1, tab2, tab3 = st.tabs(["Resultado consolidado", "Tabela de preços", "Tabela de cotas"])

with tab1:
    st.title("Evolução do patrimônio")
    
    st.subheader("Consolidado")
    consolidado = px.bar(curves_cons, x="Date", y="AUM", title="AUM Consolidado",color_discrete_sequence=["steelblue"])
    st.plotly_chart(consolidado, use_container_width=True)


    # Certifique-se de que o índice foi resetado e nome correto é usado
    curves_reset = curves.reset_index()
    
    curves_long = curves_reset.melt(
        id_vars=[curves_reset.columns[0]],  # O nome correto da coluna do índice
        var_name="Categoria",
        value_name="Valor"
    )
    
    # Criar o gráfico com todas as colunas em linhas
    st.subheader("Por classe")
    plot = px.line(
        curves_long,
        x=curves_reset.columns[0],  # Use o índice resetado no eixo x
        y="Valor",
        color="Categoria",  # Diferencia por coluna original
        title="Evolução por Categoria",
        labels={curves_reset.columns[0]: "Data", "Valor": "AUM", "Categoria": "Classe"}
    )
    st.plotly_chart(plot, use_container_width=True)


    st.subheader("Por fundo")
    fundo = px.bar(curves.reset_index(), x="index", y="Fund", title="AUM por Fundo",color_discrete_sequence=["steelblue"])
    st.plotly_chart(fundo, use_container_width=True)

with tab2:
    st.title("Informações gerais")
    st.dataframe(invest_info)

with tab3:
    st.title("Tabela de preços")
    st.dataframe(prices.sort_index(ascending=False))
