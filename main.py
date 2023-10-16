import requests
import pandas as pd
import streamlit as st


# Configurações da página
st.set_page_config(
    page_title=' Projeto API - Moedas Comemorativas',
    page_icon='🪙',
    layout='wide'
)


#Requisição API - Banco Central Do Brasil
url ='https://olinda.bcb.gov.br/olinda/servico/mecir_moedas_comemorativas/versao/v1/odata/informacoes_diarias?$top=10000&$format=json'
response = requests.get(url)
information = response.json()


# Pandas - Tratamento dos dados
df = pd.DataFrame(information['value'])
#Transformando coluna em data
df['Data'] = pd.to_datetime(df['Data'])
#Extraindo o mês
df['Mês'] = (df['Data'].dt.month)
#Extraindo o ano
df['Ano'] = (df['Data'].dt.year)
#Extraindo o dia
df['Dia'] = (df['Data'].dt.day)


#Barra lateral de navegação 
st.sidebar.header('Por favor, Filtre aqui: ')

#selecionar o mês
mes = st.sidebar.selectbox(
    'Selecione o mês: ',
    options = df['Mês'].unique()
    
)


#Selecione o ano
ano = st.sidebar.selectbox(
    'Selecione o ano: ',
    options = df['Ano'].unique()
)


#Selecionar Tipo de Moeda
categoria_moeda = st.sidebar.selectbox(
    'Selecione a categoria da moeda: ',
    options = df['Categoria'].unique()

)
st.sidebar.write('Você selecionou:', categoria_moeda)


# Consulta dos dados 
df_page = df.query(
    'Mês == @mes & Ano == @ano & Categoria == @categoria_moeda '
)


#Página Principal
st.title('🪙 Moedas Comemorativas')
st.markdown('##')


#indicador - quantidade em circulação no ano
df_quantidade_mes = df_page.groupby(['Ano', 'Categoria']).agg({'Quantidade':'sum'})
df_quantidade_mes = df_quantidade_mes['Quantidade'].sum()
#indicador - Média Quantidade em circulação no Mês 
df_quantidade_dia = df_page.groupby(['Mês', 'Categoria']).agg({'Quantidade':'mean'})
df_quantidade_dia = df_quantidade_dia['Quantidade'].mean()
#indicador - Valor 
df_valor = df_page.groupby(['Mês', 'Categoria']).agg({'Valor':'sum'})
df_valor = df_valor['Valor'].sum()


with st.container():
    st.write('Projeto criado para integrar uma API (Interface de Programação de Aplicação) do Banco Central do Brasil e realizar algumas consultas.')
    st.write('No projeto também foi aplicado algumas funcionalidades para filtrar o ano, mês e tipo da categoria da moeda comemorativa e conforme é selecionado o gráfico e os indicadores são alterados. Com o python e pandas foi possivel manipular os dados e criar os indicadores com algumas operações simples.')
    st.write('As bibliotecas utilizadas no projeto: requests, pandas e streamlit.')
    st.write('---')

    
#Colunas dos indicadores
column1, column2, column3 = st.columns(3)
with column1:
    st.subheader('📈 Quantidade em circulação no mês: ')
    st.subheader(f'{df_quantidade_mes:,}')
with column2:
    st.subheader('📆 Média em circulação por Mês: ')
    st.subheader(f'{df_quantidade_dia:.2f}')
with column3:
    st.subheader('Valor total das moedas no mês: ')
    st.subheader(f'R$: {df_valor:,.2f}') 

#Botão apagar
with st.container():
    button_apagar = st.sidebar.button('Apagar Filtro', type='primary')
    if button_apagar == True:
        st.dataframe(df)
    else:
        st.dataframe(df_page)
        
        




























