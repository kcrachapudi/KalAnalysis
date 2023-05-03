# Import the required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from path import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import Utils
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import holoviews as hv
import numpy as np
import DataFramer
import Aggridder
import BackTester

signals_df = Utils.GetCSVDataFromResources("backtest-metrics.csv", "date")

st.write(' Review the DataFrame')
st.write(signals_df.head(10))
st.write(signals_df.tail(10))
