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
    
df2 = df1.copy()
    
#=======================
#Barra Lateral Sreamlit
#=======================

st.sidebar.markdown('## Filtros')

paises =st.sidebar.multiselect('Escolha os países que deseja visualizar na página',
                               ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'],
                               default= ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

values = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar', 0, 20, 10)

culinaria =st.sidebar.multiselect('Escolha o tipo de culinária',
                               ['Home-Made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American','Italian'],
                               default= ['Home-Made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American','Italian'])

st.sidebar.markdown("___")
st.sidebar.markdown("Powered by Ilana Cruz")

#=======================
#Link base com filtros
#=======================

#filtro de país
linhas_selecionadas=df2['Country Code'].isin(paises)
df2=df2.loc[linhas_selecionadas,:]

#filtro de culinaria
linhas_selecionadas=df2['Cuisines'].isin(culinaria)
df2=df2.loc[linhas_selecionadas,:]

#========================
#Página Principal
#========================
st.markdown ('# Visão Culinária')
st.markdown ('## Melhores Restaurantes dos Principais Tipos de Culinária')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        
        
        #Melhores Restaurantes dos Principais tipos Culinários
        #1 Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
        df_comida1 = df1.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]

        comida_ita = df_comida1['Cuisines']== 'Italian'
        df_comida1 = df_comida1.loc[comida_ita, :].copy()

        df_ita_media = df_comida1.loc[:, ['Restaurant ID','Aggregate rating']].groupby(['Restaurant ID','Aggregate rating']).count().reset_index()

        so_max1 = df_ita_media['Aggregate rating'] == df_ita_media['Aggregate rating'].max()
        df_ita_media = df_ita_media.loc[so_max1, :].copy()

        rest_ita = df1['Restaurant ID'] == df_ita_media.iloc[0, 0]
        busca_rest1 = df1.loc[rest_ita,:]

        cozinha1 = busca_rest1.iloc[0,9]
        rest1 = busca_rest1.iloc[0,1]
        nota1= df_ita_media.iloc[0, 1]

        st.metric(label=f'{cozinha1}: {rest1}', value=f'{nota1}/5.0')


    with col2:
        #3 Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?

        df_comida1 = df1.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]

        comida_ame = df_comida1['Cuisines']== 'American'
        df_comida1 = df_comida1.loc[comida_ame, :].copy()

        df_ame_media = df_comida1.loc[:, ['Restaurant ID','Aggregate rating']].groupby(['Restaurant ID','Aggregate rating']).count().reset_index()

        so_max1 = df_ame_media['Aggregate rating'] == df_ame_media['Aggregate rating'].max()
        df_ame_media = df_ame_media.loc[so_max1, :].copy()

        rest_ame = df1['Restaurant ID'] == df_ame_media.iloc[0, 0]
        busca_rest3 = df1.loc[rest_ame,:]

        cozinha2 = busca_rest3.iloc[0,9]
        rest2 = busca_rest3.iloc[0,1]
        nota2= df_ame_media.iloc[0, 1]
        st.metric(label=f'{cozinha2}: {rest2}', value=f'{nota2}/5.0')


    with col3:
        #5 Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?

        df_comida1 = df1.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]

        comida_ara = df_comida1['Cuisines']== 'Arabian'
        df_comida1 = df_comida1.loc[comida_ara, :].copy()

        df_ara_media = df_comida1.loc[:, ['Restaurant ID','Aggregate rating']].groupby(['Restaurant ID','Aggregate rating']).count().reset_index()

        so_max1 = df_ara_media['Aggregate rating'] == df_ara_media['Aggregate rating'].max()
        df_ara_media = df_ara_media.loc[so_max1, :].copy()

        rest_ara = df1['Restaurant ID'] == df_ara_media.iloc[0, 0]
        busca_rest5 = df1.loc[rest_ara,:]

        cozinha3 = busca_rest5.iloc[0,9]
        rest3 = busca_rest5.iloc[0,1]
        nota3= df_ara_media.iloc[0, 1]
        st.metric(label=f'{cozinha3}: {rest3}', value=f'{nota3}/5.0')
       
    with col4:
        #7 Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
        df_comida1 = df1.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]

        comida_jap = df_comida1['Cuisines']== 'Japanese'
        df_comida1 = df_comida1.loc[comida_jap, :].copy()

        df_jap_media = df_comida1.loc[:, ['Restaurant ID','Aggregate rating']].groupby(['Restaurant ID','Aggregate rating']).count().reset_index()

        so_max1 = df_jap_media['Aggregate rating'] == df_jap_media['Aggregate rating'].max()
        df_jap_media = df_jap_media.loc[so_max1, :].copy()

        rest_jap = df1['Restaurant ID'] == df_jap_media.iloc[0, 0]
        busca_rest7 = df1.loc[rest_jap,:]

        cozinha4 = busca_rest7.iloc[0,9]
        rest4 = busca_rest7.iloc[0,1]
        nota4= df_jap_media.iloc[0, 1]
        st.metric(label=f'{cozinha4}: {rest4}', value=f'{nota4}/5.0')
        
    with col5:
        #9 Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?

        df_comida1 = df1.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]

        comida_cas = df_comida1['Cuisines']== 'Home-made'
        df_comida1 = df_comida1.loc[comida_cas, :].copy()

        df_cas_media = df_comida1.loc[:, ['Restaurant ID','Aggregate rating']].groupby(['Restaurant ID','Aggregate rating']).count().reset_index()

        so_max1 = df_cas_media['Aggregate rating'] == df_cas_media['Aggregate rating'].max()
        df_cas_media = df_cas_media.loc[so_max1, :].copy()

        rest_cas = df1['Restaurant ID'] == 5914190
        busca_rest9 = df1.loc[rest_cas,:]

        cozinha5 = busca_rest9.iloc[0,9]
        rest5 = busca_rest9.iloc[0,1]
        nota5= df_cas_media.iloc[0, 1]
        st.metric(label=f'{cozinha5}: {rest5}', value=f'{nota5}/5.0')
        
#Top #20 restaurantes (tabela)
with st.container():
    df_maior_nota = df2.loc[:, ['Restaurant ID','Restaurant Name','Country Code','City','Cuisines','Average Cost for two','Aggregate rating','Votes']].groupby(['Restaurant ID','Restaurant Name','Country Code','City','Cuisines','Average Cost for two','Aggregate rating','Votes']).count().reset_index()

    busca_maior_nota= df_maior_nota.sort_values (['Aggregate rating'], ascending= False).head(values)
    
    st.markdown (f'### Top {values} Restaurantes')
    st.table(data=busca_maior_nota)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        #Top 10 melhores culinárias
     
        st.markdown (f'Top {values} Melhores Tipos de Culinária')
        df_nota_12 = df2.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]
        df_nota_12 = np.round(df_nota_12.loc[:, ['Cuisines','Aggregate rating']].groupby(['Cuisines']).mean().reset_index(),2)

        busca_melhor_culinária= df_nota_12.sort_values (['Aggregate rating'], ascending= True).reset_index()
        top10 = busca_melhor_culinária.iloc[-10:,:]


        fig_melhores= px.bar (top10, x= 'Aggregate rating', y= 'Cuisines', text_auto=True, labels={'Aggregate rating':'Avaliações médias'})
        st.plotly_chart(fig_melhores, use_container_width=True)

    with col2:
        #Top 10 piores culinárias

        st.markdown (f'Top {values} Piores Tipos de Culinária')
        df_nota_12 = df2.loc[:, ['Restaurant ID','Aggregate rating','Cuisines']]
        df_nota_12 = np.round(df_nota_12.loc[:, ['Cuisines','Aggregate rating']].groupby(['Cuisines']).mean().reset_index(), 2)

        busca_pior_culinária= df_nota_12.sort_values (['Aggregate rating'], ascending= False).reset_index()

        top10 = busca_pior_culinária.iloc[-10:,:]
        fig_piores= px.bar (top10, x= 'Aggregate rating', y= 'Cuisines', text_auto=True, labels={'Aggregate rating':'Avaliações médias'})
        st.plotly_chart(fig_piores, use_container_width=True)