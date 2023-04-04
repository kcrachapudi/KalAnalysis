"""Crypto Clustering"""

"""
In this project we combine financial Python with unsupervised learning to help cluster Crypto Currencies.

The crypto currency data provided contains price change data of cryptocurrencies in different periods.

The steps for the analysis are broken out into the following sections:

* Import the Data 
* Prepare the Data 
* Find the Best Value for `k` Using the Original Data
* Cluster Cryptocurrencies with K-means Using the Original Data
* Optimize Clusters with Principal Component Analysis
* Find the Best Value for `k` Using the PCA Data
* Cluster the Cryptocurrencies with K-means Using the PCA Data
* Visualize and Compare the Results
"""


""" Import the Data
This section imports the data into a new DataFrame. It follows these steps:

1. Read  the crypto market data into a DataFrame and Review the DataFrame.

2. Generate the summary statistics, and use HvPlot to visualize your data to observe what your DataFrame contains.
"""

# Import required libraries and dependencies
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

# Load the data into a Pandas DataFram
df_market_data = Utils.GetCSVDataFromResources("crypto_market_data.csv", "coin_id")

# Display sample data
if df_market_data is not None:
    st.write(df_market_data.head(10))