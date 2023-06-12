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
st.markdown ('# Visão Cidade')

with st.container():
    st.markdown("##### Top 10 cidades com mais restaurantes")
    #gráfico qtde rest X cidade -gráfico de barras: alterar a cor por país
    df_mais_rest1= df1.loc[:, ['Country Code','City', 'Restaurant ID']].groupby(['Country Code','City']).count().reset_index()

    ordena_cidade= df_mais_rest1.sort_values (['Restaurant ID', 'City'], ascending= True)
    ordena_cidade = ordena_cidade.iloc[-10:,:]
    fig1= px.bar (ordena_cidade, x= 'Restaurant ID', y= 'City', text_auto=True, color='Country Code', labels={'Restaurant ID':'Quantidade de restaurante'})
    st.plotly_chart(fig1, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        #gráfico qtde rest avaliaçao >4 X cidade
        st.markdown("##### Top 7 cidades com restaurantes cujas médias de avaliação são superiores a 4")
        df_cidade_rest_nt = df1.loc[:, ['Country Code','City','Aggregate rating', 'Restaurant ID']].groupby(['Restaurant ID', 'Country  Code','City','Aggregate rating']).count().reset_index()

        so_nota= df_cidade_rest_nt['Aggregate rating'] > 4
        df_cidade_rest_nt = df_cidade_rest_nt.loc[so_nota, :].copy()

        df_cidade_rest_nt = df_cidade_rest_nt.loc[:, ['Country Code','City', 'Restaurant ID']].groupby(['Restaurant ID','Country Code', 'City']).count().reset_index()
        df_cidade_rest_nt = df_cidade_rest_nt.loc[:, ['Country Code','City', 'Restaurant ID']].groupby(['City', 'Country Code']).count().reset_index()

        ordena_cidade= df_cidade_rest_nt.sort_values (['Restaurant ID', 'City'], ascending= True)
        ordena_cidade = ordena_cidade.iloc[-10:,:]
        fig2=px.bar (ordena_cidade, x= 'Restaurant ID', y= 'City', text_auto=True, color='Country Code', labels={'Restaurant ID':'Quantidade de restaurante'})
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        #gráfico qtde rest avaliaçao <2.5 X cidade
        st.markdown("##### Top 7 cidades com restaurantes cujas médias de avaliação são inferiores a 2,5")
        df_cidade_rest_nt = df1.loc[:, ['Country Code','City','Aggregate rating', 'Restaurant ID']].groupby(['Restaurant ID', 'Country Code','City','Aggregate rating']).count().reset_index()

        so_nota= df_cidade_rest_nt['Aggregate rating'] < 2.5
        df_cidade_rest_nt = df_cidade_rest_nt.loc[so_nota, :].copy()

        df_cidade_rest_nt = df_cidade_rest_nt.loc[:, ['Country Code','City', 'Restaurant ID']].groupby(['Restaurant ID','Country Code', 'City']).count().reset_index()
        df_cidade_rest_nt = df_cidade_rest_nt.loc[:, ['Country Code','City', 'Restaurant ID']].groupby(['City', 'Country Code']).count().reset_index()

        ordena_cidade= df_cidade_rest_nt.sort_values (['Restaurant ID', 'City'], ascending= True)
        ordena_cidade = ordena_cidade.iloc[-10:,:]
        fig3=px.bar (ordena_cidade, x= 'Restaurant ID', y= 'City', text_auto=True, color='Country Code', labels={'Restaurant ID':'Quantidade de restaurante'})
        st.plotly_chart(fig3, use_container_width=True)

with st.container():
    #gráfico qtde tipos de culinaria X cidade
    st.markdown("##### Top 10 cidades com restaurantes com mais tipos de culinárias distintas")
    df_mais_culi5 = df1.loc[:, ['City','Country Code', 'Cuisines']].groupby(['Country Code','City','Cuisines']).count().reset_index()
    df_mais_culi5 =df_mais_culi5.loc[:, ['City','Country Code', 'Cuisines']].groupby(['Country Code','City']).count().reset_index()

    ordena_cidade= df_mais_culi5.sort_values (['Cuisines', 'City'], ascending= True)
    ordena_cidade = ordena_cidade.iloc[-10:,:]
    fig4=px.bar (ordena_cidade, x= 'Cuisines', y= 'City', text_auto=True, color='Country Code', labels={'Cuisines':'Quantidade de tipos de culinária únicos'})
    st.plotly_chart(fig4, use_container_width=True)