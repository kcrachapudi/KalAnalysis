# Import the required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import DataPreparer, cloud_data_collector, StockPredictor
import holoviews as hv
from Utilities import Utils
import numpy as np
import datetime
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report

st.write(
"""
## Stock Price Predictor
"""
)
ticker = st.text_input("Enter the Ticker you need Analysis")
if ticker:
    dfTrades = Utils.GetLocalTickerData(ticker=ticker, location=None)
    if(dfTrades is None or dfTrades.empty):
        st.write('No data found in local location. Downloading from Yahoo Finance')
    dfTrades = cloud_data_collector.GetYFTickerHistory(ticker=ticker, historyperiod='5y')   
    if(dfTrades is None or dfTrades.empty):
        st.write('No data found in Yahoo Finance. Please check the ticker name')
        st.stop()
    else:
        st.write('Data downloaded from Yahoo Finance')
        st.write(dfTrades.head())
        st.write(dfTrades.tail())
        Utils.SaveTickerData(ticker=ticker, dfTicker=dfTrades, location=None)
        st.write('Data saved to local location')

st.write(' Preparing the Data ')
closeColName = 'Close'
dfTrades = DataPreparer.PrepareBasicEquityCloseData(dfData=dfTrades, closeCol=closeColName)
st.write(dfTrades.head())
st.write(dfTrades.tail())
st.write('Data prepared')
#tabPredRSI, tabPredBBands, tabPredMACD, tabPredAllLSTM, tabPredAllBLSTM = st.tabs(["RSI", 'BBands', 'MACD', 'AllLSTM', 'AllBLSTM'])
# Grid layout
c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

dfPredRSI = pd.DataFrame()
dfPredRSI['Date'] = dfTrades['Date']
with c1:
    dfPredRSI = StockPredictor.GeneratePrediction(dfData=dfTrades, technicalindicator='RSI', scaler='MinMaxScaler', model='Bidirectional LSTM + Attention')
    st.print(txtBrokerageAccountName = st.text_input("RSI Brokerage Account")
with c2:
    txtCash = st.text_input("Cash")
with c3:
    txtMarginUsed = st.text_input("Margin Used")
with c4:
    txtMarginBuyingPower = st.text_input("Margin Buying Power")
with c5:
    txtDayTradeBuyingPower = st.text_input("Day Trade Buying Power")
with c6:
    txtDayTradeBuyingPower1 = st.text_input("Day Trade Buying Power1")
