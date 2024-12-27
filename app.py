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
tab1, tab2, tab3, tab4 = st.tabs(["Evolução", "Composição", "Tabela de preços", "Tabela de cotas"])

with tab1:
    st.title("Evolução do patrimônio")
    
    consolidado = px.bar(curves_cons, x="Date", y="AUM", title="AUM Consolidado",color_discrete_sequence=["green"], labels={"Date": ""})
    st.plotly_chart(consolidado, use_container_width=True)

    
    dict_names = dict(zip(invest_info['Bloomberg ID'], invest_info['Tipo']))
    curves_grouped = curves.rename(dict_names, axis=1)
    curves_grouped = curves_grouped.groupby(curves_grouped.columns, axis=1).sum()
    curves_classe = curves_grouped.reset_index()
    curves_classe = curves_classe.melt(id_vars=[curves_classe.columns[0]],var_name="Categoria",value_name="Valor")
    plot = px.line(curves_classe,x=curves_classe.columns[0],y="Valor",color="Categoria",title="Evolução por Categoria",labels={curves_classe.columns[0]: "", "Valor": "AUM", "Categoria": "Classe"})
    st.plotly_chart(plot, use_container_width=True)

    dict_names = dict(zip(invest_info['Bloomberg ID'], invest_info['Fundo']))
    curves_inv = curves.rename(dict_names, axis=1).fillna(0).reset_index()
    curves_inv = curves_inv.melt(id_vars=[curves_inv.columns[0]],var_name="Categoria",value_name="Valor")
    plot = px.line(curves_inv,x=curves_inv.columns[0],y="Valor",color="Categoria",title="Evolução por Investimento",labels={curves_inv.columns[0]: "", "Valor": "AUM", "Categoria": "Investimento"})
    st.plotly_chart(plot, use_container_width=True)


with tab2:
    st.title("Composição")
        
    dict_names = dict(zip(invest_info['Bloomberg ID'], invest_info['Tipo']))
    curves_grouped = curves.rename(dict_names, axis=1)
    curves_grouped = curves_grouped.groupby(curves_grouped.columns, axis=1).sum()
    latest_values_classe = curves_grouped.iloc[-1]  # Última linha agrupada por classe
    classe_pizza = px.pie(
        names=latest_values_classe.index,  # Nomes das categorias
        values=latest_values_classe.values,  # Valores da última linha
        title="Proporção por Classe",
        hole=0.4
    )
    st.plotly_chart(classe_pizza, use_container_width=True)


    dict_names = dict(zip(invest_info['Bloomberg ID'], invest_info['Fundo']))
    curves_inv = curves.rename(dict_names, axis=1).fillna(0)
    latest_values_inv = curves_inv.iloc[-1]  # Última linha agrupada por fundo
    inv_pizza = px.pie(
        names=latest_values_inv.index,  # Nomes das categorias
        values=latest_values_inv.values,  # Valores da última linha
        title="Proporção por Investimento",
        hole=0.4
    )
    st.plotly_chart(inv_pizza, use_container_width=True)



with tab3:
    st.title("Informações gerais")
    st.dataframe(invest_info)


with tab4:
    st.title("Tabela de preços")
    st.dataframe(prices.sort_index(ascending=False))
