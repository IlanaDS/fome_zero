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

st.sidebar.markdown('## Filtro')

paises =st.sidebar.multiselect('Escolha os países que deseja visualizar na página',
                               ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'],
                               default= ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

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
st.markdown ('# Visão País')

#Gráfico qtde rest X país
with st.container():
    st.markdown('###### Quantidade de restaurantes registrados por país')
    df_mais_rest= df1.loc[:, ['Country Code', 'Restaurant ID']].groupby('Country Code').count().reset_index()
    ordena_pais= df_mais_rest.sort_values (['Restaurant ID', 'Country Code'], ascending= True)

    fig1= px.bar (ordena_pais, x= 'Restaurant ID', y= 'Country Code', text_auto=True, labels={'Restaurante ID':'Quantidade de restaurante'})
    st.plotly_chart(fig1, use_container_width=True)

#Gráfico qtde cidade X país
with st.container():
    st.markdown('###### Quantidade de cidades registradas por país')
    df_pais_cidades = df1.loc[:, ['Country Code', 'City']].groupby(['Country Code', 'City']).count().reset_index()
    df_mais_cidades= df_pais_cidades.loc[:, ['Country Code', 'City']].groupby('Country Code').count().reset_index()

    ordena_pais= df_mais_cidades.sort_values (['City', 'Country Code'], ascending= True)

    fig2 = px.bar (ordena_pais, x= 'City', y= 'Country Code', text_auto=True, labels={'City':'Quantidade de cidades'})
    st.plotly_chart(fig2, use_container_width=True)

with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        #Gráfico qtde avaliações X país
        st.markdown('###### Média de avaliações feitas por país')
        df_mais_aval = df1.loc[:, ['Country Code','Votes']].groupby(['Country Code','Votes']).count().reset_index()
        df_mais_aval1 =df_mais_aval.loc[:, ['Country Code','Votes']].groupby('Country Code').mean().reset_index()

        ordena_pais= df_mais_aval1.sort_values (['Votes', 'Country Code'], ascending= True)

        fig3= px.bar (ordena_pais, x= 'Votes', y= 'Country Code', text_auto=True, labels={'Votes':'Quantidade de avaliações'})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        #Gráfico preço para 2  X país
        st.markdown('###### Média de preços de prato para duas pessoas por país')
        df_media_prato2 = df1.loc[:, ['Country Code','Average Cost for two']].groupby(['Country Code','Average Cost for two']).count().reset_index()
        df_media_prato2 = df_media_prato2.loc[:, ['Country Code','Average Cost for two']].groupby('Country Code').mean().reset_index()

        ordena_pais= df_media_prato2.sort_values (['Average Cost for two', 'Country Code'], ascending= True)

        fig4=px.bar (ordena_pais, x= 'Average Cost for two', y= 'Country Code', text_auto=True, labels={'Average Cost for two':'Preço prato para duas pessoas'})
        st.plotly_chart(fig4, use_container_width=True)