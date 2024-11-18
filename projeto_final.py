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

st.title('Dashboard de Deputados por Estado e Gênero')

#Selectbox para filtrar por gênero
genero = st.selectbox('Selecione o Gênero', ['Todos', 'Mulheres', 'Homens'])

# Multiselect para filtrar por múltiplas UFs (estados)
ufs_selecionadas = st.multiselect('Selecione as UFs (Estados)', ['Todos'] + df_todos['siglaUf'].unique().tolist(), default=['Todos'])

# Criar uma cópia do DataFrame original para evitar a modificação direta de df_todos
df_filtrado = df_todos.copy()

#Aplicar filtros de gênero e UF
if genero != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['siglaSexo'] == genero]

if 'Todos' not in ufs_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['siglaUf'].isin(ufs_selecionadas)]

#Contar o número de deputados por estado e gênero
contagem_estados = df_filtrado.groupby(['siglaUf']).size().unstack(fill_value=0)

#Criar DataFrame consolidado para análise
df_estados = contagem_estados.rename(columns={'F': 'Mulheres', 'M': 'Homens'})

# Calcular total de deputados
total_deputados = df_filtrado.shape[0]

# Calcular porcentagens de homens e mulheres
porcentagem_mulheres = (contagem_estados['F'].sum() / total_deputados) * 100 if total_deputados > 0 else 0
porcentagem_homens = (contagem_estados['M'].sum() / total_deputados) * 100 if total_deputados > 0 else 0

# Exibir informações no Streamlit
st.write(f'Total de Deputados Filtrados: {total_deputados}')
st.write(f'Porcentagem de Mulheres: {porcentagem_mulheres:.2f}%')
st.write(f'Porcentagem de Homens: {porcentagem_homens:.2f}%')

# Verificar se df_estados contém dados numéricos
if df_estados.isnull().values.any():
    st.error("Os dados para o gráfico estão ausentes ou mal formatados. Verifique os dados.")

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


