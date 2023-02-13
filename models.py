import yfinance as yf
import pandas as pd
import cv2
from pathlib import Path
import os


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

    return cripto.drop(columns=['Volume','Dividends','Stock Splits'])


def get_dolar():
    dolar = yf.Ticker('USDBRL=X').history(interval='30m',period='2h').sort_values(by='Datetime', ascending=True)
    return dolar['Close']


def trasnform_USDxBRL(df):
    dolar = get_dolar()
    dolar = dolar[len(dolar)-1]
    df['Open'] = df['Open'].map(lambda x: x*dolar)
    df['High'] = df['High'].map(lambda x: x*dolar)
    df['Low'] = df['Low'].map(lambda x: x*dolar)
    df['Close'] = df['Close'].map(lambda x: x*dolar)
    return df


def load_RNASR():

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # dir = Path(__file__).resolve().parent
    # dir = os.path.join(dir, 'ESPCN_X4.pb')
    # print(dir)
    sr.readModel('modelos/ESPCN_x4.pb')
    # sr.setModel("espcn",4)

    return 'ok'