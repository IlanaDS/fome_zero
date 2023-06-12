from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import numpy  as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Import dataset
df = pd.read_csv( 'zomato.csv' )
df1 = df.copy()

#print (df1.head(5))

#==============================Limpeza de dados===========================================
# Excluir as linhas das colunas vazias 

#linhas_selecionadas = (df1['Cuisines'] != 'NaN') 
#df1 = df1.loc[linhas_selecionadas, :].copy()
df1=df1.loc[df1['Cuisines'].notnull(),:]


#filtros Cuisines solicitado pelo CEO
df1['Cuisines'] = df1.loc[:, 'Cuisines'].astype(str).apply(lambda x: x.split(',')[0])


#filtros realizados pela CDS:
linhas_selecionadas = (df1['Cuisines'] != 'Mineira') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas1 = (df1['Cuisines'] != 'Drinks Only') 
df1 = df1.loc[linhas_selecionadas1, :].copy()

#Recategorização de cor solicitada pelo CEO
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
  return COLORS[color_code]

df1['Rating color'] = df1['Rating color'].apply(color_name)


#Recategorização de paises solicitada pelo CEO
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
  return COUNTRIES[country_id]

df1['Country Code'] = df1['Country Code'].apply(country_name)


#Recategorização de preços solicitada pelo CEO
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

df1['Price range'] = df1['Price range'].apply(create_price_tye)  

#Categorizações sugeridas pelo CEO

def rename_columns(dataframe):
  df =dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df1.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df

  df1 = df1.apply(rename_columns)  
    
#=======================
#Barra Lateral Sreamlit
#=======================

#image_path= 'alvo.jpg'
#image=Image.open(image_path)
#st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero')

st.sidebar.markdown('## Filtro')

paises =st.sidebar.multiselect('Escolha os países que deseja visualizar na página',
                               ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'],
                               default= ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

st.sidebar.markdown('## Dados Tratados')

def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df1)

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='df1',
    mime='text/csv',
)


st.sidebar.markdown("""---""")
st.sidebar.markdown("Powered by Ilana Cruz")

#=======================
#Link base com filtros
#=======================

#filtro de país
linhas_selecionadas=df1['Country Code'].isin(paises)
df1=df1.loc[linhas_selecionadas,:]

#========================
#Página Principal
#========================

st.markdown ('# Fome Zero')
st.markdown ('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown ('### Temos as seguintes marcas dentro da nossa plataforma:')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        rest_unicos = df1.loc[:, 'Restaurant ID'].nunique()
        st.markdown ('###### Restaurantes Cadastrados')
        st.markdown (rest_unicos)

    with col2:
        paises_unicos = df1.loc[:, 'Country Code'].nunique()
        st.markdown ('###### Países Cadastrados')
        st.markdown (paises_unicos)
        
    with col3:       
        cidades_unicas = df1.loc[:, 'City'].nunique()
        st.markdown ('###### Cidades Cadastradas')
        st.markdown (cidades_unicas)

    with col4:
        df_votes= df1.loc[:, ['Votes', 'Restaurant ID']].groupby(['Restaurant ID','Votes']).count().reset_index()
        df_votes= df_votes['Votes'].sum()
        st.markdown ('###### Avaliações Feitas na Plataforma')
        st.markdown (df_votes)

    with col5:
        culinarias = df1.loc[:, 'Cuisines'].nunique()
        st.markdown ('###### Cozinhas           ')
        st.markdown (culinarias)

fig = folium.Figure(width=1920, height=1080)
m = folium.Map(max_bounds=True).add_to(fig)
marker_cluster = MarkerCluster().add_to(m)

for _, line in df1.iterrows():

    folium.Marker(
        location=(line['Latitude'], line['Longitude']),
        icon=folium.Icon(color=line['Rating color'], icon='pushpin')).add_to(marker_cluster)
    
folium_static(m)
    
