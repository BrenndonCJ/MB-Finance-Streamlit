import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

from models import get_data, trasnform_USDxBRL, get_dolar


def generate_graph(df, x, colunas, subtitle='Cripto'):
    fig = px.line(
        df,
        x=x,
        y=colunas,
        color=subtitle,
        title=None,
        line_dash=None,
        labels={'Hour':'Hora','Date':'Data', 'value':'Preço'},
        markers=True,
    )
    
    fig.update_layout(plot_bgcolor = 'RGBA(255,255,255,0)')
    fig.update_xaxes( showgrid=False, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='white', title=None)
    fig.update_yaxes(showgrid=False, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='white')
    return fig


dict_criptos = {
    'POLYGON':'MATIC-USD',
    'ETHEREUM':'ETH-USD',
    'SOLANA':'SOL-USD',
    'POLKADOT':'DOT-USD',
    'AVALANCHE':'AVAX-USD',
    'THE SANDBOX':'SAND-USD',
    'CARDANO':'ADA-USD',
    'STELLAR':'XLM-USD',
    'DECENTRALAND':'MANA-USD',
    'AXIE INFINITY':'AXS-USD',
    'UNISWAP':'UNI7083-USD',
}

dict_periodo = {
    '24 horas':'1d',
    '7 dias':'7d',
    '15 dias':'15d',
    '30 dias':'30d',
    '90 dias':'90d',
    '6 meses':'6mo',
    '1 ano':'1y',
    '2 anos':'2y',
    'Maximo':'max',
}

dict_intervalos = {
    '5 minutos':'5m',
    '30 minutos':'30m',
    '1 hora':'1h',
}

df_cripto = pd.DataFrame()

# Elementos

st.set_page_config(
         page_icon="",
         page_title="MB Finance",
         layout="wide",
         initial_sidebar_state="expanded"
)

#SideBar
st.sidebar.title("Aplicativos")

# Page MB Finance
st.title('MB Finance')

# Colunas
dolar_cols = st.columns([4,1])

dolar_cols[0].warning("Fuso horario GMT 0 = Compense diminuindo 3hrs para o Brasil")

# Elemento Dolar
dolar = get_dolar()
if dolar[len(dolar)-1] >= dolar[len(dolar)-2]:
    dolar_cols[len(dolar_cols)-1].success(f" 1 Dolar = R$ {dolar[len(dolar)-1]:.2f}⬆️", icon="💲")
else:
    dolar_cols[len(dolar_cols)-1].error(f" 1 Dolar = R$ {dolar[len(dolar)-1]:.2f}⬇️", icon="💲")

# Definindo guias para multiplos graficos na mesma pagina
guias_graficos = st.tabs(['Geral', 'Moeda Unica'])

with guias_graficos[1]:

    # Colunas guias_graficos[1]
    guias_graficos0_colunas = guias_graficos[1].columns(3)

    opt_cripto = guias_graficos0_colunas[0].selectbox(
        label='Selecione uma criptomoeda',
        options=sorted(dict_criptos.keys()),
    )

    opt_dias = guias_graficos0_colunas[1].selectbox(
        label='Selecione o intervalo de tempo',
        options=dict_periodo.keys(),
    )

    if dict_periodo[opt_dias] == '1d':
        opt_intervalo = guias_graficos0_colunas[2].selectbox(
            label='Selecione o intervalo de tempo',
            options=dict_intervalos.keys(),
            index=0
        )
        cripto = get_data(dict_criptos[opt_cripto], coin_name=opt_cripto ,interval=dict_intervalos[opt_intervalo], period=dict_periodo[opt_dias])
    else:
        cripto = get_data(dict_criptos[opt_cripto], coin_name=opt_cripto ,period=dict_periodo[opt_dias])

    cripto = trasnform_USDxBRL(cripto)

    # Criando graficos
    colunas = ['Close','Open']
    inform = f"Valores {opt_cripto}:"

    if dict_periodo[opt_dias] == '1d':
        fig1 = generate_graph(cripto, 'Hour', colunas, subtitle=None)
    else:
        fig1 = generate_graph(cripto, 'Date', colunas, subtitle=None)

    j1, j2 = st.columns([4,1])
    
    with j1:
        st.subheader(opt_cripto)
        # Plotando graficos
        st.plotly_chart(fig1, use_container_width=True, config=dict(displayModeBar=False))

    with j2:
        if cripto['Close'][len(cripto)-1] >= cripto['Close'][len(cripto)-2]:
            st.success(f" R$ {cripto['Close'][len(cripto)-1]:.2f}⬆️", icon="🪙")
        else:
            st.error(f"R$ {cripto['Close'][len(cripto)-1]:.2f}⬇️", icon="🪙")
############################### GUIA 1 #####################################
with guias_graficos[0]:

    # Colunas guias_graficos[1]
    guias_graficos1_colunas = st.columns(3)

    opt_cripto = guias_graficos1_colunas[0].multiselect(
        label='Selecione uma criptomoeda',
        options=sorted(dict_criptos.keys()),
    )

    opt_dias = guias_graficos1_colunas[1].selectbox(
        label='Selecione o intervalo de tempo',
        options=dict_periodo.keys(),
        key=dict_periodo[opt_dias]
    )
    
    if dict_periodo[opt_dias] == '1d':
        opt_intervalo = guias_graficos1_colunas[2].selectbox(
            label='Selecione o intervalo de tempo',
            options=dict_intervalos.keys(),
            index=0,
            key='interval'
        )

    my_bar = st.progress(0)
    if opt_cripto:
        bar_controll = 100 / len(opt_cripto) /100
        increment = 100 / len(opt_cripto) /100

    for coin in opt_cripto:
        if dict_periodo[opt_dias] == '1d':
            cripto = get_data(dict_criptos[coin], coin_name=coin , interval=dict_intervalos[opt_intervalo], period=dict_periodo[opt_dias])
        else:
            cripto = get_data(dict_criptos[coin], coin_name=coin , period=dict_periodo[opt_dias])
        
        df_cripto = pd.concat([df_cripto, cripto], ignore_index=True)
        my_bar.progress(bar_controll)
        if bar_controll + increment <= 1:
            bar_controll += increment

    if opt_cripto:
        df_cripto = trasnform_USDxBRL(df_cripto)

    # Criando graficos
    colunas = ['Close']
    inform = f"Valores {opt_cripto}:"

    if opt_cripto:
        if dict_periodo[opt_dias] == '1d':
            fig1 = generate_graph(df_cripto, 'Hour', colunas)
        else:
            fig1 = generate_graph(df_cripto, 'Date', colunas)

        # Plotando graficos
        st.plotly_chart(fig1, use_container_width=True, config=dict(displayModeBar=False))
    else:
        st.write("Selecione alguma(s) moeda(s)")

# st.info('This is a purely info message', icon="ℹ️")
# st.success('This is a purely sucess message', icon="ℹ️")
# st.error('This is a purely error message', icon="ℹ️")
# st.warning('This is a purely warning message', icon="ℹ️")