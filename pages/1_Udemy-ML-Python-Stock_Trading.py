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

#@st.cache_resource #Run this only Once
def init():
    # Algorithm to Predict Tomorrow's Stock Direction (Up or Down) based on Past Data
    st.session_state.ticker = stc.Custom_TextInput("Ticker", '', 'txtTicker')
    st.session_state.startYear = stc.Custom_TextInput("Start Year", '', 'txtStartYear')
    st.session_state.table1 = st.container()
    st.session_state.table1.markdown("...")
    st.session_state.table2 = st.container()
    st.session_state.table2.markdown("...")
    st.session_state.chart1 = st.container()
    st.session_state.chart1.markdown("...")
    
init()


def DownloadAndProcessData(startYear, ticker):
    #Download Historical Data
    startdate= startYear + '-01-01'
    enddate=date.today()
    dfData:pd.DataFrame = yf.download(ticker, start=startdate, end=enddate, progress=False)

    stc.Container_AddDataframe(container=st.session_state.table1, dfData=dfData, printType='head')
    #st.write(dfData.head())
    #Remove Ticker row from Column Name
    dfData = dfData.droplevel(1, axis=1)

    # Rename the columns using the dictionary
    rename_dict = {'Close': 'close', 'Volume': 'volume', 'High':'high', 'Open':'open', 'Low':'low'}
    dfData.rename(columns=rename_dict, inplace=True)

    #Chart the Stock Performance
    stc.Container_AddDataframe(container=st.session_state.table1, dfData=dfData, printType='head')
    #st.write(dfData.head())
    #st.line_chart(dfData, y='close')
    stc.Container_AddChart(container=st.session_state.chart1, chart=px.line(dfData, y='close'))

       
def SubmitClick():
    if st.session_state.ticker is  None or len(st.session_state.ticker) == 0 or st.session_state.startYear is None or len(st.session_state.startYear) == 0:
        st.session_state.ticker = st.session_state["txtTicker"]
        st.session_state.startYear = st.session_state['txtStartYear']
    DownloadAndProcessData(st.session_state.startYear, st.session_state.ticker)
           
stc.Custom_Button(label="DownloadAndProcessData", key='btnSubmit', action=SubmitClick)


