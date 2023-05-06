# Import the required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import BackTestFinal, BackTestInitial, Utils
import holoviews as hv
import numpy as np
import Aggridder

dfTrades:pd.DataFrame = Utils.GetCSVDataFromResources("ml_ohlcv.csv", "Date")

st.write(' Review the DataFrame')
st.write(dfTrades.head())
st.write(dfTrades.tail())

st.write('Use the Pandas pct_change function to calculate the daily returns from the closing prices. We assign these values to a new column named “actual_returns”, as the following code shows:')
st.write(' Calculate the daily returns using the closing prices and the pct_change function')
dfTrades["ActualReturns"] = dfTrades["Close"].pct_change()
st.write(dfTrades.head())

st.write(' Drop all NaN values from the DataFrame')
dfTrades = dfTrades.dropna()
st.write(dfTrades.head())


st.text_area('Create the Features Set', " Think back to the dual moving average crossover (DMAC) trading algorithm that you generated in the previous lessons. You used a single trading signal to determine the entry and exit points for the algorithm. (That trading signal was the crossover point between the short-window and long-window SMAs.) The lesson demonstrations used the data to generate trading signals for holding long positions. By contrast, the activities used the trading signals to initiate short-position trades—first selling stock and then buying it to cover the sale, ideally at a lower price. For our machine learning–powered trading algorithm, the trading signals will make up the features set.")
st.text_area('ML2', "Our new trading algorithm will continue to use the same short- and long-window SMA logic, but with a slight difference. We’ll create an SMA column using a window size of 4 days, and name it “sma_fast”. We’ll create another SMA column using a window size of 100 days, and name it sma_slow")

st.write("We start by creating the sma_fast column in our DataFrame, as the following code shows:")
st.write('# Define a short window size')
short_window = 4

st.write(' Create an SMA that uses short_window, and assign it to a new column named “sma_fast”')
dfTrades['SMAFast'] = dfTrades['Close'].rolling(window=short_window).mean()

st.write('Similarly, we create the “sma_slow” column in our DataFrame, as the following code shows:')
st.write(' Define a long window size')
long_window = 100
st.write('Create an SMA that uses long_window, and assign it to a new column named “sma_slow” ')
dfTrades['SMASlow'] = dfTrades['Close'].rolling(window=long_window).mean()

st.write('Drop all the NaN values by using the dropna function, as the following code shows:')
dfTrades = dfTrades.dropna()

st.text_area('ML3', "Finally, we create the X features set by copying the “sma_fast” and “sma_slow” columns from our original DataFrame into a new DataFrame named X. However, we want the model to learn a predictive relationship. (That is, we want to know how “sma_fast” and “sma_slow” will predict returns in the future.) We’ll thus use the shift function to shift the feature columns by 1. Doing so ensures that the model will use the current values to predict the outcome for the next period.")
st.write('The following code creates the X features set and shifts the columns:')
st.write(' Assign a copy of the `sma_fast` and `sma_slow` columns to a new DataFrame called X')
X = dfTrades[['SMAFast', 'SMASlow']].shift().dropna().copy()
st.write('Display sample data')
st.write(X.head())
