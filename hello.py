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
