import yfinance as yf
import pandas as pd
import cv2
from pathlib import Path
import os
from pickle import load
# from sklearn.preprocessing import MinMaxScaler
# import streamlit as st


def get_data(coin, coin_name='', interval='1d', period='1d'):
    cripto = yf.Ticker(coin).history(interval=interval,period=period)
    try:
        cripto = cripto.sort_values(by='Datetime', ascending=True)
    except:
        cripto = cripto.sort_values(by='Date', ascending=True)

    cripto['Coin'] = coin
    cripto['Cripto'] = coin_name
    cripto['Date'] = cripto.index.strftime('%d/%m/%y')
    cripto['Hour'] = cripto.index.strftime('%H:%M')

    # return cripto.drop(columns=['Volume','Dividends','Stock Splits'])
    return cripto


def get_dolar():
    dolar = yf.Ticker('USDBRL=X').history(interval='30m',period='1d')#.sort_values(by='Datetime', ascending=True)
    return dolar['Close']


def transform_USDxBRL(df):
    dolar = get_dolar()
    dolar = dolar[len(dolar)-1]
    df['Open'] = df['Open'].map(lambda x: x*dolar)
    df['High'] = df['High'].map(lambda x: x*dolar)
    df['Low'] = df['Low'].map(lambda x: x*dolar)
    df['Close'] = df['Close'].map(lambda x: x*dolar)
    return df


# @st.cache(persist=True,allow_output_mutation=True,show_spinner=False,suppress_st_warning=True)
def load_RNASR():

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # dir = Path(__file__).resolve().parent
    # dir = os.path.join(dir, 'ESPCN_X4.pb')
    sr.readModel('modelos/ESPCN_x4.pb')
    sr.setModel("espcn",4)

    return sr

def estimative_value(features, coin):
    normalize = load(open(f'modelos/{coin}_normalize.pkl'.lower(),'rb'))
    model = load(open(f'modelos/{coin}_model.pkl'.lower(),'rb'))

    features = normalize.transform(features)
    pred = model.predict(features)
    
    return f'R${pred[0]:.2f}'


def bandas_bollinger(df):
    # Calcular media movel
    media_movel = df[['Close']].rolling(window=20).mean()
    desvio_padrao = df[['Close']].rolling(window=20).std()
    banda_superior = media_movel + 2 * desvio_padrao
    banda_superior = banda_superior.rename(columns={'Close':'Superior'})
    banda_inferior = media_movel - 2 * desvio_padrao
    banda_inferior = banda_inferior.rename(columns={'Close':'Inferior'})
    df = df.join(banda_superior).join(banda_inferior)
    return df.dropna()