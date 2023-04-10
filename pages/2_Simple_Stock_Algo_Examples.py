import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import cloud_data_collector
import Utils
import Models
import plotly.graph_objects as go
from plotly.subplots import make_subplots

""" Simple Stock Trade Algorithms"""

ticker = None
tickerdetails = None

def Init():
    ticker = GetSelectedTicker()
    lstTickers = [ticker]
    tickerdetails = cloud_data_collector.GetTickersData(lstTickers, '1y')      
    tabSimpleStockAlgo1, tabSimpleStockAlgo2 = st.tabs(["DailyBuySell", "DailyBuySellLast"])
    with tabSimpleStockAlgo1:
        st.dataframe(tickerdetails, 700, 300)
    with tabSimpleStockAlgo2:
        pass

def GetSelectedTicker():
        ticker = 'NVDA'
        return ticker


Init()