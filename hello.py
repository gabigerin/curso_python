import streamlit as st
st.write("Sou servidora pública")

import requests as req

url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome'
response = req.get(url)

dados = response.json()

import matplotlib.pyplot as plt

df_camara['siglaPartido'].value_counts().plot(kind='bar')
plt.show()
