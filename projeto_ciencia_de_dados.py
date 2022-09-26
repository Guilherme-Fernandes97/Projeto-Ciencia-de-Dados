# Importar Bibliotecas e Bases de Dados

import pandas as pd
import pathlib
import numpy as np

meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}

caminho_bases = pathlib.Path('dataset')

base_airbnb = pd.DataFrame()

for arquivo in caminho_bases.iterdir():
    nome_mes = arquivo.name[:3]
    mes = meses[nome_mes]

    ano = arquivo.name[-8:]
    ano = int(ano.replace('.csv', ''))

    df = pd.read_csv(caminho_bases / arquivo.name)
    df['ano'] = ano
    df['mes'] = mes
    base_airbnb = pd.concat([base_airbnb, df])



# Removendo colunas desnecessarias para o modelo de previsão
# Para isso vamos criar um arquivo em excel com os 1.000 registros e fazer uma análise qualitativa
# Remover colunas parecidas

base_airbnb.head(1000).to_csv('primeiros_registros.csv', sep=';')

colunas = ['host_is_superhost','host_listings_count','latitude','longitude','property_type','room_type','accommodates','bathrooms','bedrooms','beds','bed_type','amenities','price','guests_included','extra_people','minimum_nights','number_of_reviews','instant_bookable','is_business_travel_ready','cancellation_policy','ano','mes','maximum_nights']

base_airbnb = base_airbnb.loc[:, colunas]

for coluna in base_airbnb:
    if base_airbnb[coluna].isnull().sum() > 300000:
        base_airbnb = base_airbnb.drop(coluna, axis=1)

base_airbnb = base_airbnb.dropna()

#alterando preço e extra_people para float (esta sendo reconhecido como objeto)
base_airbnb['price'] = base_airbnb['price'].str.replace('$', '')
base_airbnb['price'] = base_airbnb['price'].str.replace(',', '')
base_airbnb['price'] = base_airbnb['price'].astype(np.float32, copy=False)

base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace('$', '')
base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace(',', '')
base_airbnb['extra_people'] = base_airbnb['extra_people'].astype(np.float32, copy=False)

print(base_airbnb.dtypes)