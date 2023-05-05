# Import the required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import BackTestFinal, BackTestInitial, Utils
import holoviews as hv
import numpy as np
import Aggridder

dfSignals:pd.DataFrame = Utils.GetCSVDataFromResources("backtest-metrics.csv", "date")

st.write(' Review the DataFrame')
st.write(dfSignals.head(10))
st.write(dfSignals.tail(10))

dfInitialEvaluated = BackTestInitial.Evaluate(dfSignals=dfSignals)

dfFinalEvaluated = BackTestFinal.Evaluate(dfData=dfSignals)

st.write('Note: We often consider a trading algorithm to be good if it consistently maximizes its gains while minimizing its losses. A Sharpe ratio that’s greater than 1 and a trading accuracy that’s greater than 80% are popular baselines.')