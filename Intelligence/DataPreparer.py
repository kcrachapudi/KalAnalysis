import pandas as pd
from pathlib import Path
import numpy as np
import datetime
import streamlit as st

def PrepareBasicEquityCloseData(dfData:pd.DataFrame, closeCol='close') -> pd.DataFrame:
    #Use the Pandas pct_change function to calculate the daily returns from the closing prices. We assign these values to a new column named “actual_returns”, as the following code shows:')
    # Calculate the daily returns using the closing prices and the pct_change function')
    dfData["ActualReturns"] = dfData[closeCol].pct_change()
    st.write(dfData.head())

    # Drop all NaN values from the DataFrame
    dfData = dfData.dropna()
    return dfData
