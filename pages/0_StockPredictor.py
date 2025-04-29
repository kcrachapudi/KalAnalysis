# Import the required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import DataPreparer, cloud_data_collector
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
tabPredRSI, tabPredBBands, tabPredMACD, tabPredAllLSTM, tabPredAllBLSTM = st.tabs(["RSI", 'BBands', 'MACD', 'AllLSTM', 'AllBLSTM'])
