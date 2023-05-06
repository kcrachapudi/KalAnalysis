import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from Algos import Algo_Stock_Long_Simple_DailyBuySell, Algo_Stock_Long_Simple_DailyBuySellLast
import cloud_data_collector
from Intelligence import Utils
import Models
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Algos import *

st.write(
"""
# KalAnalysis.com
Fun AI based Quant Stock and Crypto Analysis to analyze trends and predict outcomes.
"""
)


""" Simple Stock Long Trade Algorithms"""

ticker = None
tickerdetails = None
TotalProfitLoss = 0

def Init():
    ticker = GetSelectedTicker()
    lstTickers = [ticker]
    dfTicker = Utils.GetLocalTickerData(ticker=ticker)

    if(dfTicker is None):
        print(f'Loading ticker data for ticker {ticker}')
        dfTicker = cloud_data_collector.GetTickersData(lstTickers, '1y')  
        if(dfTicker is not None):
            Utils.SaveTickerData(ticker, dfTicker)

    if(dfTicker is None):
        st.write(f"Error loading data for ticker {ticker}.")             
    else:
        st.dataframe(dfTicker, 1000, 300)
        tabSimpleStockAlgo1, tabSimpleStockAlgo2 = st.tabs(["DailyBuySell", "DailyBuySellLast"])
        with tabSimpleStockAlgo1:
            dfTicker, TotalProfitLoss, InvestedCapital, ROI = Algo_Stock_Long_Simple_DailyBuySell.Init(dfTicker)
            st.dataframe(dfTicker, 1000, 300)
            st.write(f"The total profit/loss of the trading strategy is ${TotalProfitLoss}.")
            st.write(f"The Invested Capital of the trading strategy is ${InvestedCapital}.")
            st.write(f"The Return on Investment of the algorithm is {ROI}%")
        with tabSimpleStockAlgo2:
            dfTicker2, TotalProfitLoss2, InvestedCapital2, ROI2 = Algo_Stock_Long_Simple_DailyBuySellLast.Init(dfTicker)
            st.dataframe(dfTicker2, 1000, 300)
            st.write(f"The total profit/loss of the trading strategy is ${TotalProfitLoss2}.")
            st.write(f"The Invested Capital of the trading strategy is ${InvestedCapital2}.")
            st.write(f"The Return on Investment of the algorithm is {ROI2}%")

def GetSelectedTicker():
        ticker = 'NVDA'
        return ticker


Init()