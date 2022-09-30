# Importar Bibliotecas e Bases de Dados

import pandas as pd
import pathlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11,
         'dez': 12}

caminho_bases = pathlib.Path('dataset')

base_airbnb = pd.DataFrame()

for arquivo in caminho_bases.iterdir():
    nome_mes = arquivo.name[:3]
    mes = meses[nome_mes]

    ano = arquivo.name[-8:]
    ano = int(ano.replace('.csv', ''))

    df = pd.read_csv(caminho_bases / arquivo.name, low_memory=False)
    df['ano'] = ano
    df['mes'] = mes
    base_airbnb = pd.concat([base_airbnb, df])

# Removendo colunas desnecessarias para o modelo de previsão
# Para isso vamos criar um arquivo em excel com os 1.000 registros e fazer uma análise qualitativa
# Remover colunas parecidas

base_airbnb.head(1000).to_csv('primeiros_registros.csv', sep=';')

colunas = ['host_is_superhost', 'host_listings_count', 'latitude', 'longitude', 'property_type', 'room_type',
           'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities', 'price', 'guests_included',
           'extra_people', 'minimum_nights', 'number_of_reviews', 'instant_bookable', 'is_business_travel_ready',
           'cancellation_policy', 'ano', 'mes', 'maximum_nights']

base_airbnb = base_airbnb.loc[:, colunas]

for coluna in base_airbnb:
    if base_airbnb[coluna].isnull().sum() > 300000:
        base_airbnb = base_airbnb.drop(coluna, axis=1)

base_airbnb = base_airbnb.dropna()

# alterando preço e extra_people para float (esta sendo reconhecido como objeto)
base_airbnb['price'] = base_airbnb['price'].str.replace('$', '', regex=True)
base_airbnb['price'] = base_airbnb['price'].str.replace(',', '')
base_airbnb['price'] = base_airbnb['price'].astype(np.float32)

base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace('$', '', regex=True)
base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace(',', '')
base_airbnb['extra_people'] = base_airbnb['extra_people'].astype(np.float32)

# Análise Exploratória e Tratar Outliers

''' Ver a correlação entre as features e decidir se manteremos todas as features que temos. Excluir outliers (usaremos
 como regra, valores abaixo de Q1 - 1.5xAmplitude e valores acima de Q3 + 1.5x Amplitude). Amplitude = Q3 - Q1
 Confirmar se todas as features que temos fazem realmente sentido para o nosso modelo ou se alguma delas não vai nos
 ajudar e se devemos excluir '''

plt.figure(figsize=(15, 10))
sns.heatmap(base_airbnb.corr(), annot=True, cmap='Greens')


# Definição de funções para análise de outliers

def limites(coluna):
    q1 = coluna.quantile(0.25)
    q3 = coluna.quantile(0.75)
    amplitude = q3 - q1
    return q1 - 1.5 * amplitude, q3 + 1.5 * amplitude


def diagrama_caixa(coluna):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(15, 5)
    sns.boxplot(x=coluna, ax=ax1)
    ax2.set_xlim(limites(coluna))
    sns.boxplot(x=coluna, ax=ax2)


def histograma(coluna):
    plt.figure(figsize=(15, 5))
    sns.histplot(coluna)

def grafico_barra(coluna):
    plt.figure(figsize=(15, 5))
    ax = sns.barplot(x=coluna.value_counts().index, y=coluna.value_counts())
    ax.set_xlim(limites(coluna))

# Definição de função para excluir outliers


def excluir_outliers(df, nome_coluna):
    qtde_linhas = df.shape[0]
    lim_inf, lim_sup = limites(df[nome_coluna])
    df = df.loc[(df[nome_coluna] >= lim_inf) & (df[nome_coluna] <= lim_sup), :]
    linhas_removidas = qtde_linhas - df.shape[0]
    return df, linhas_removidas

# Análise dos outliers de preço

# diagrama_caixa(base_airbnb['price'])
# histograma(base_airbnb['price'])


base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, 'price')
print(f'{linhas_removidas} Linhas removidas')

# Análise dos outliers de extra people

# diagrama_caixa(base_airbnb['extra_people'])
# histograma(base_airbnb['extra_people'])

base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, 'extra_people')
print(f'{linhas_removidas} Linhas removidas')

# Análise dos outliers de host_listings_count

diagrama_caixa(base_airbnb['host_listings_count'])
grafico_barra(base_airbnb['host_listings_count'])

base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, 'host_listings_count')
print(f'{linhas_removidas} Linhas removidas')

plt.show()

