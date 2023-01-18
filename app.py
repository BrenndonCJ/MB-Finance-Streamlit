import streamlit as st
import yfinance as yf
import plotly.express as px

from bot_telegram import send_message
from time import sleep
from threading import Thread


def send_message_telegram():
    while True:
        try:
            criptomoeda = yf.Ticker('MATIC-USD').history(period='1d')
            criptomoeda['Close'] = criptomoeda['Close'].map(lambda x: x*dolar)
            last_value = criptomoeda['Close'][0]
            message = f"Ultimo fechamento da MATIC: R$ {last_value:.2f}".replace('.',',')
            send_message(message=message)
            sleep(3.600)
        except:
            pass

# Elementos
#SideBar
opt_cripto = st.sidebar.selectbox(
    'Selecione uma criptomoeda',
    ('MATIC-USD', 'ADA-USD', 'UNI7083-USD')
)
opt_dias = st.sidebar.selectbox(
    'Selecione o intervalo de tempo',
    ('7 dias', '15 dias', '30 dias', '60 dias', '90 dias')
)

dolar = yf.Ticker('USDBRL=X').history(period='1d').sort_values(by='Date', ascending=False)
dolar = dolar['Close'][0]

cripto = yf.Ticker(opt_cripto).history(period=opt_dias.replace(' ','').replace('ias','')).sort_values(by='Date', ascending=True)

cripto['Open'] = cripto['Open'].map(lambda x: x*dolar)
cripto['High'] = cripto['High'].map(lambda x: x*dolar)
cripto['Low'] = cripto['Low'].map(lambda x: x*dolar)
cripto['Close'] = cripto['Close'].map(lambda x: x*dolar)
cripto.index = cripto.index.strftime('%d/%m/%y')

# Criando graficos
colunas = ['Open', 'High', 'Low', 'Close']
inform = f"Valores {opt_cripto}:"
fig1 = px.line(cripto, x=cripto.index, y=colunas, title=inform, line_dash=None)
fig1.update_layout(plot_bgcolor = '#0E1117')
fig1.update_xaxes( showgrid=False, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='white')
fig1.update_yaxes(showgrid=False, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='white')

# Elementos
# Body
st.title('MB Finance')
#st.write(cripto)
st.subheader(opt_cripto)
# st.dataframe(cripto)



# Plotando graficos
st.plotly_chart(fig1, use_container_width=True)