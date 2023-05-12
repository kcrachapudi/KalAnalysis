# Import the required libraries and dependencies
import imp
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import BackTestFinal, BackTestInitial, Utils, DataPreparer
import holoviews as hv

import numpy as np
import Intelligence.Aggridder as Aggridder
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report
from AIML import Fin_AI_SMA_Algo

st.write(
"""
## Machine Learning Algorithm - DMAC with Backtest
"""
)
dfTrades:pd.DataFrame = Utils.GetCSVDataFromResources("ml_ohlcv.csv", "Date")

st.write(' Review the DataFrame')
st.write(dfTrades.head())
st.write(dfTrades.tail())

st.write(' Preparing the Data ')
dfTrades = DataPreparer.PrepareBasicEquityCloseData(dfData=dfTrades)
st.write(dfTrades.head())

dfTabParams = pd.DataFrame({"ShortWindow":[4, 50, 20],
                   "LongWindow":[100, 100, 90],
                   "TrainPeriodMonths":[3, 3, 3],
                   "ModelType":["SVM", "SVM", "SVM"],
                   "UIComponentPrefix":["Tab1", "Tab2", "Tab3"]})

algosma4and100, algosma50and100, algosma20and90 = st.tabs(["AlgoSMA4and100", "AlgoSMA50and100", 'AlgoSMA20and90'])

with algosma4and100:
    Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades, 
                                 shortWindow=dfTabParams.at[0, 'ShortWindow'], 
                                 longWindow=dfTabParams.at[0, 'LongWindow'],
                                 model_type=dfTabParams.at[0, 'ModelType'], 
                                 train_data_period_months=dfTabParams.at[0, 'TrainPeriodMonths'],
                                 ui_component_prefix=dfTabParams.at[0, 'UIComponentPrefix'])
with algosma50and100:
    Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades, 
                                 shortWindow=dfTabParams.at[1, 'ShortWindow'], 
                                 longWindow=dfTabParams.at[1, 'LongWindow'],
                                 model_type=dfTabParams.at[1, 'ModelType'], 
                                 train_data_period_months=dfTabParams.at[1, 'TrainPeriodMonths'],
                                 ui_component_prefix=dfTabParams.at[1, 'UIComponentPrefix'])
with algosma20and90:
    Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades, 
                                 shortWindow=dfTabParams.at[2, 'ShortWindow'], 
                                 longWindow=dfTabParams.at[2, 'LongWindow'],
                                 model_type=dfTabParams.at[2, 'ModelType'], 
                                 train_data_period_months=dfTabParams.at[2, 'TrainPeriodMonths'],
                                 ui_component_prefix=dfTabParams.at[2, 'UIComponentPrefix'])
