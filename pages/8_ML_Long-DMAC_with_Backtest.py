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

dfTrades:pd.DataFrame = Utils.GetCSVDataFromResources("ml_ohlcv.csv", "Date")

st.write(' Review the DataFrame')
st.write(dfTrades.head())
st.write(dfTrades.tail())

st.write(' Preparing the Data ')
dfTrades = DataPreparer.PrepareBasicEquityCloseData(dfData=dfTrades)
st.write(dfTrades.head())

Fin_AI_SMA_Algo.FinAISMAAlgo(trades_df=dfTrades,  shortWindow=4, longWindow=100,model_type="SVM", train_data_period_months=3)
