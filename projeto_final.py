import streamlit as st
import requests as req
import pandas as pd
import matplotlib.pyplot as plt

#Obter os dados de mulheres
url_mulheres = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=siglaUF'
response_mulheres = req.get(url_mulheres)
dados_mulheres = response_mulheres.json()

#Criar DataFrame para mulheres
df_mulheres = pd.DataFrame(dados_mulheres['dados'])

#Obter os dados de homens
url_homens = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=siglaUF'
response_homens = req.get(url_homens)
dados_homens = response_homens.json()

#Criar DataFrame para homens
df_homens = pd.DataFrame(dados_homens['dados'])

#Adicionar a coluna 'siglaSexo' antes de concatenar
df_mulheres['siglaSexo'] = 'F'
df_homens['siglaSexo'] = 'M'

#Concatenar os DataFrames
df_todos = pd.concat([df_mulheres, df_homens], ignore_index=True)

#Contar o número de deputados por estado e gênero
contagem_estados = df_todos.groupby(['siglaUf', 'siglaSexo']).size().unstack(fill_value=0)

#Criar DataFrame consolidado para análise
df_estados = contagem_estados.rename(columns={'F': 'Mulheres', 'M': 'Homens'})

#Gráfico de barras usando Matplotlib
fig, ax = plt.subplots(figsize=(12, 8))

graf = df_estados.plot(kind='bar', ax=ax, color=['darkorchid', 'limegreen'], edgecolor='none', alpha=0.85)
ax.set_title('Número de Deputados por Estado e Gênero', fontsize=18, fontweight='bold', color='#333333')
ax.set_xlabel('Estado', fontsize=14, labelpad=10, fontweight='bold', color='#333333')
ax.set_ylabel('Número de Deputados', fontsize=14, labelpad=10, fontweight='bold', color='#333333')
ax.legend(title='Gênero', fontsize=12, title_fontsize=14, loc='best', frameon=True, shadow=True, facecolor='white')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=12, ha='right')
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=45)

#Mostrar o gráfico no Streamlit
st.pyplot(fig)

# Streamlit
st.title('Dashboard de Deputados por Estado e Gênero')

# Selectbox para filtrar por gênero
gênero = st.selectbox('Selecione o Gênero', ['Todos', 'Mulheres', 'Homens'])

# Filtrar os dados de acordo com a seleção
if gênero != 'Todos':
    df_todos = df_todos[df_todos['siglaSexo'] == gênero]

# Contar o número de deputados por estado e gênero
contagem_estados = df_todos.groupby(['siglaUf', 'siglaSexo']).size().unstack(fill_value=0)

# Criar DataFrame consolidado para análise
df_estados = contagem_estados.rename(columns={'F': 'Mulheres', 'M': 'Homens'})

# Gráfico de barras
fig, ax = plt.subplots(figsize=(12, 8))

# Plotar o gráfico de barras
bars = df_estados.plot(kind='bar', ax=ax, color=['#4CAF50', '#2196F3'], edgecolor='white', alpha=0.85)

# Ajustar os títulos e eixos
ax.set_title('Número de Deputados por Estado e Gênero', fontsize=18, fontweight='bold', color='#333333')
ax.set_xlabel('Estado', fontsize=14, labelpad=10, fontweight='bold', color='#333333')
ax.set_ylabel('Número de Deputados', fontsize=14, labelpad=10, fontweight='bold', color='#333333')

# Adicionar números em cima das barras
for p in bars.patches:
    height = p.get_height()  # Obtém a altura de cada barra (valor da barra)
    ax.text(p.get_x() + p.get_width() / 2, height + 0.1, str(int(height)), ha='center', fontsize=12, color='black')

# Adicionar legenda
ax.legend(title='Gênero', fontsize=12, title_fontsize=14, loc='best', frameon=True, shadow=True, facecolor='white')

# Ajustar rótulos do eixo X
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=12, ha='right')

# Melhorias no gráfico
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Mostrar o gráfico no Streamlit
st.pyplot(fig)
