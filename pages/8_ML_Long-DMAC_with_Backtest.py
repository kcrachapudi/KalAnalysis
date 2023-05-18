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

dfTrades:pd.DataFrame = Utils.GetCSVDataFromResources("ohlcv.csv", "date")

st.write(' Review the DataFrame')
st.write(dfTrades.head())
st.write(dfTrades.tail())

st.write(' Preparing the Data ')
dfTrades = DataPreparer.PrepareBasicEquityCloseData(dfData=dfTrades)
st.write(dfTrades.head())
st.write(dfTrades.tail())

initialCapital = 100000

st.write('##SVM Model')
dfTabParams = pd.DataFrame({"ShortWindow":[4, 50, 20],
                   "LongWindow":[100, 100, 90],
                   "TrainPeriodMonths":[3, 3, 3],
                   "ModelType":["SVM", "SVM", "SVM"],
                   "UIComponentPrefix":["svmTab1", "svmTab2", "svmTab3"]})
algosma4and100, algosma50and100, algosma20and90 = st.tabs(["AlgoSMA4and100", "AlgoSMA50and100", 'AlgoSMA20and90'])
with algosma4and100:
    algosma1 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades,
                                 closeColName='close',
                                 shortWindow=dfTabParams.at[0, 'ShortWindow'], 
                                 longWindow=dfTabParams.at[0, 'LongWindow'],
                                 model_type=dfTabParams.at[0, 'ModelType'], 
                                 train_data_period_months=dfTabParams.at[0, 'TrainPeriodMonths'],
                                 initCapital=initialCapital,
                                 ui_component_prefix=dfTabParams.at[0, 'UIComponentPrefix'])
with algosma50and100:
    algosma2 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades,
                                closeColName='close',
                                shortWindow=dfTabParams.at[1, 'ShortWindow'], 
                                longWindow=dfTabParams.at[1, 'LongWindow'],
                                model_type=dfTabParams.at[1, 'ModelType'], 
                                train_data_period_months=dfTabParams.at[1, 'TrainPeriodMonths'],
                                initCapital=initialCapital,
                                ui_component_prefix=dfTabParams.at[1, 'UIComponentPrefix'])
with algosma20and90:
    algosma3 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades, 
                                 closeColName='close',
                                 shortWindow=dfTabParams.at[2, 'ShortWindow'], 
                                 longWindow=dfTabParams.at[2, 'LongWindow'],
                                 model_type=dfTabParams.at[2, 'ModelType'], 
                                 train_data_period_months=dfTabParams.at[2, 'TrainPeriodMonths'],
                                 initCapital=initialCapital,
                                 ui_component_prefix=dfTabParams.at[2, 'UIComponentPrefix'])

st.write('##Logistic Regression Model')
dfTabParams2 = pd.DataFrame({"ShortWindow":[4, 50, 20],
                   "LongWindow":[100, 100, 90],
                   "TrainPeriodMonths":[3, 3, 3],
                   "ModelType":["LogisticRegression", "LogisticRegression", "LogisticRegression"],
                   "UIComponentPrefix":["lrTab1", "lrTab2", "lrTab3"]})
algo2sma4and100, algo2sma50and100, algo2sma20and90 = st.tabs(["AlgoSMA4and100", "AlgoSMA50and100", 'AlgoSMA20and90'])
with algo2sma4and100:
    algo2sma1 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades,
                                 closeColName='close',
                                 shortWindow=dfTabParams2.at[0, 'ShortWindow'], 
                                 longWindow=dfTabParams2.at[0, 'LongWindow'],
                                 model_type=dfTabParams2.at[0, 'ModelType'], 
                                 train_data_period_months=dfTabParams2.at[0, 'TrainPeriodMonths'],
                                 initCapital=initialCapital,
                                 ui_component_prefix=dfTabParams2.at[0, 'UIComponentPrefix'])
with algo2sma50and100:
    algo2sma2 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades,
                                 closeColName='close',
                                 shortWindow=dfTabParams2.at[1, 'ShortWindow'], 
                                 longWindow=dfTabParams2.at[1, 'LongWindow'],
                                 model_type=dfTabParams2.at[1, 'ModelType'], 
                                 train_data_period_months=dfTabParams2.at[1, 'TrainPeriodMonths'],
                                 initCapital=initialCapital,
                                 ui_component_prefix=dfTabParams2.at[1, 'UIComponentPrefix'])
with algo2sma20and90:
    algo2sma3 = Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades, 
                                 closeColName='close',
                                 shortWindow=dfTabParams2.at[2, 'ShortWindow'], 
                                 longWindow=dfTabParams2.at[2, 'LongWindow'],
                                 model_type=dfTabParams2.at[2, 'ModelType'], 
                                 train_data_period_months=dfTabParams2.at[2, 'TrainPeriodMonths'],
                                 initCapital=initialCapital,
                                 ui_component_prefix=dfTabParams2.at[2, 'UIComponentPrefix'])
