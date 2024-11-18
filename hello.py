import streamlit as st
st.write("Sou servidora pública")

import pandas as pd

df = pd.DataFrame({
    'nomeServidor': ['Adriana', 'Monica', 'Samara'],
    'salario': [1200,300,5000]
})

st.write("Criando uma tabela!")
st.write(df)
opcao = st.selectbox(
    'Qual servidor você gostaria de selecionar?',
     df['nomeServidor'])

st.write('Você selecionou: ', opcao)

dadosFiltrados = df[df['nomeServidor'] == opcao]
st.write(dadosFiltrados)


st.title('Localização das comunidades quilombolas (2022)')
df = pd.read_csv('https://raw.githubusercontent.com/adrianalite/datasets/main/BR_LQs_CD2022.csv')

numero = st.slider('Selecione um número', min_value = 0, max_value = 100)
st.text("Seu número é " + str(numero))


df.drop(columns=['Unnamed: 0'], inplace=True)
list = ['Lat_d', 'Long_d']
# convertendo para numeros
df[list] = df[list].apply(pd.to_numeric, errors='coerce')
estados = df['NM_UF'].unique()
estadoFiltro = st.selectbox(
    'Qual estado selecionar?',
     estados)
dadosFiltrados = df[df['NM_UF'] == estadoFiltro]
if st.checkbox('Mostrar tabela'):
  st.write(dadosFiltrados)
st.map(dadosFiltrados, latitude="Lat_d", longitude="Long_d")

qtdeMunicipios = len(df['NM_MUNIC'].unique())
st.write("A quantidade de municípios com localização quilombola é " + str(qtdeMunicipios))

qtdeComunidades = len(df['NM_AGLOM'].unique())
st.write("A quantidade de comunidades quilombolas é " + str(qtdeComunidades))

st.header('Número de comunidades por UF')
st.bar_chart(df['NM_UF'].value_counts())

st.header('Os dez municípios com mais comunidades quilombolas')
st.bar_chart(df['NM_MUNIC'].value_counts()[:10])

numero = st.slider('Selecione um número de linhas a serem exibidas', min_value = 0, max_value = 100)
st.write(df.head(numero))

st.metric('# Municípios', len(df['NM_MUNIC'].unique()))
st.metric('# Comunidades', len(df['NM_AGLOM'].unique()))

import requests as req
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome'
response = req.get(url)
dados = response.json()

import pandas as pd
df_camara = pd.DataFrame(dados['dados'])

import matplotlib.pyplot as plt

df_camara['siglaPartido'].value_counts().plot(kind='bar')
plt.show()

