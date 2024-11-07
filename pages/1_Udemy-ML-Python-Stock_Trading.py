import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import date, time
#Install Yahoo Finance Libraries
import yfinance as yf
import yahoofinancials as YahooFinancials
from StreamlitExtras import StreamlitControls as stc
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.session_state.ticker = None
st.session_state.startYear = None
ticker = None
startYear = None

def init():
    # Algorithm to Predict Tomorrow's Stock Direction (Up or Down) based on Past Data
    st.session_state.ticker = stc.Custom_TextInput("Ticker", '', 'txtTicker')
    st.session_state.startYear = stc.Custom_TextInput("Start Year", '', 'txtStartYear')
    

def DownloadAndProcessData(startYear, ticker):
    #Download Historical Data
    startdate= startYear + '-01-01'
    enddate=date.today()
    dfData:pd.DataFrame = yf.download(ticker, start=startdate, end=enddate, progress=False)

    st.write(dfData.head())
    #Remove Ticker row from Column Name
    dfData = dfData.droplevel(1, axis=1)

    # Rename the columns using the dictionary
    rename_dict = {'Close': 'close', 'Volume': 'volume', 'High':'high', 'Open':'open', 'Low':'low'}
    dfData.rename(columns=rename_dict, inplace=True)

    #Chart the Stock Performance
    st.write(dfData.head())
    st.line_chart(dfData, y='close')

init()
       
def SubmitClick():
    if st.session_state.ticker is  None or len(st.session_state.ticker) == 0 or st.session_state.startYear is None or len(st.session_state.startYear) == 0:
        st.session_state.ticker = st.session_state["txtTicker"]
        st.session_state.startYear = st.session_state['txtStartYear']
    DownloadAndProcessData(st.session_state.startYear, st.session_state.ticker)
           
stc.Custom_Button(label="DownloadAndProcessData", key='btnSubmit', action=SubmitClick)


