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

st.title('Dashboard de Deputados por Estado')

# Selectbox para filtrar por múltiplos sexos
genero = st.multiselect('Selecione o(s) Gênero(s)', ['Mulheres', 'Homens'])

# Fazer uma cópia do DataFrame original para filtrar sem alterar o original
df_filtrado = df_todos.copy()

# Aplicar filtro de gênero
if genero:
    if 'Mulheres' in genero and 'Homens' in genero:
        # Quando ambos são selecionados, não altera df_filtrado (incluir todos)
        pass
    elif 'Mulheres' in genero:
        df_filtrado = df_filtrado[df_filtrado['siglaSexo'] == 'F']
    elif 'Homens' in genero:
        df_filtrado = df_filtrado[df_filtrado['siglaSexo'] == 'M']

# Contar o número de deputados por estado
contagem_estados = df_filtrado.groupby('siglaUf').size()

# Criar DataFrame consolidado para análise
df_estados = pd.DataFrame(contagem_estados).rename(columns={0: 'Número de Deputados'})

# Verificar se o DataFrame df_estados tem dados
st.write(df_estados)  # Adicione esta linha para ver o conteúdo de df_estados
if df_estados.empty:
    st.error("Não há dados para plotar. Verifique os filtros aplicados.")
else:
    # Calcular total de deputados
    total_deputados = df_filtrado.shape[0]

    # Calcular porcentagens de deputados por estado
    porcentagem_deputados = (contagem_estados.sum() / total_deputados) * 100 if total_deputados > 0 else 0

    # Exibir informações no Streamlit
    st.write(f'Total de Deputados Filtrados: {total_deputados}')
    st.write(f'Porcentagem de Deputados Selecionados: {porcentagem_deputados:.2f}%')

    # Gráfico de barras usando Matplotlib
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotando o gráfico
    graf = df_estados.plot(kind='bar', ax=ax, color='darkorchid', edgecolor='none', alpha=0.85)

    # Configurações do gráfico
    ax.set_title('Número de Deputados por Estado', fontsize=18, fontweight='bold', color='#333333')
    ax.set_xlabel('Estado', fontsize=14, labelpad=10, fontweight='bold', color='#333333')
    ax.set_ylabel('Número de Deputados', fontsize=14, labelpad=10, fontweight='bold', color='#333333')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=12, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)

    # Criar o slider para selecionar o número de linhas a serem exibidas
    numero = st.slider('Selecione o número de linhas a serem exibidas', min_value=0, max_value=len(df_todos))

    # Exibir as primeiras 'numero' linhas do DataFrame df_todos
    st.write(df_todos.head(numero))
