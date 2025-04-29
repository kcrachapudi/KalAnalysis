import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from Intelligence import DataFramer, BackTester
import holoviews as hv
import numpy as np
import Intelligence.Aggridder as Aggridder
from Utilities import Utils

with st.spinner('Retrieving and loading Stock Data...'):
    st.write("CSV Data loaded into DataFrame")
    df_market_data = Utils.GetCSVDataFromResources("aapl.csv", "date")
    if df_market_data is not None:
        st.write('Sample of Original Data')
        st.write(df_market_data.head())
        st.write(df_market_data.tail())
        st.write('Filter the date index and close columns')
        signals_df = df_market_data.loc[:,["close"]]
        st.write('Sample of Signals DF')
        st.write(signals_df.head())
        st.write('Plot of Signals DF')
        dfPlot = signals_df.hvplot.line(
            height=600,
            rot=90,
            responsive=True
        )
        st.write(hv.render(dfPlot, backend='bokeh'))
        # Set the variables for short window and long window periods
        short_window = 50
        long_window = 100
        st.write('Generate the short and long window simple moving averages 50 and 100 days, respectively')
        signals_df["SMA50"] = signals_df["close"].rolling(window=short_window).mean()
        signals_df["SMA100"] = signals_df["close"].rolling(window=long_window).mean()

        st.write('Review the Signals DataFrame after adding 50 and 100 day rolling SMA')
        st.write(signals_df.head())
        st.write(signals_df.tail())
        # Create a column to hold the trading signal
        signals_df["Signal"] = 0.0
        st.write('Generate the trading signal 0 or 1, where 1 is the short-window (SMA50) greater than the long-window (SMA100) and 0 is when the condition is not met')
        signals_df["Signal"][short_window:] = np.where(
            signals_df["SMA50"][short_window:] > signals_df["SMA100"][short_window:], 1.0, 0.0
        )
        st.write('Review the Signals DataFrame after setting the Signal')
        st.write(signals_df.tail(10))
        st.write('Calculate the points in time when the Signal value changes Identify trade entry (1) and exit (-1) points')
        signals_df["Entry/Exit"] = signals_df["Signal"].diff()
        st.write('Review the Signals DataFrame with Entry/Exit')
        #signals_df.loc["2015-02-09":"2015-02-17"]
        st.write(signals_df.tail(30))
        st.write('Visualize exit position relative to close price')
        exitplot = signals_df[signals_df['Entry/Exit'] == -1.0]['close'].hvplot.scatter(
            color="red",
            legend=False,
            ylabel='Price in $',
            width=1000,
            height=400,
            marker='v')

        # Show the plot
        st.write(hv.render(exitplot, backend='bokeh'))

        st.write('Visualize entry position relative to close price')
        entryplot = signals_df[signals_df['Entry/Exit'] == 1.0]['close'].hvplot.scatter(
            color='green',
            legend=False,
            ylabel='Price in $',
            width=1000,
            height=400,
            marker='^')

        # Show the plot
        st.write(hv.render(entryplot, backend='bokeh'))

        st.write('Visualize close price for the investment')
        closeplot = signals_df[['close']].hvplot.line(
            line_color="lightgray",
            ylabel="Close Price",
            width=1000,
            height=400)
        st.write(hv.render(closeplot, backend='bokeh'))

        st.write('Visualize moving averages')
        moving_avgs_plot = signals_df[['SMA50', 'SMA100']].hvplot.line(
            ylabel='Close Price',
            width=1000,
            height=400)
        st.write(hv.render(moving_avgs_plot, backend='bokeh'))

        st.write('Create the overlay plot')
        full_plot = closeplot * moving_avgs_plot * entryplot * exitplot
        full_plot.opts(title="SMA50, SMA100, Entry and Exit Points")
        st.write(hv.render(full_plot, backend='bokeh'))

        # Set initial capital
        initial_capital = float(100000)
        st.write(f'Initial Capital is {initial_capital}')
        # Set the share size
        share_size = 500
        st.write(f'ShareSize is {share_size}')

        BackTester.BackTesterInit(dfData=signals_df, initialCapital=initial_capital, shareSize=share_size)

        st.write('Completed Analysis')