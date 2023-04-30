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
        st.write('BackTest Processing of Algorithm...')
        # Buy a 500 share position when the dual moving average crossover Signal equals 1 (SMA50 is greater than SMA100)
        # Sell a 500 share position when the dual moving average crossover Signal equals 0 (SMA50 is less than SMA100)
        signals_df['Position'] = share_size * signals_df['Signal']

        # Determine the points in time where a 500 share position is bought or sold
        signals_df['TradePosition'] = signals_df['Position'].diff()

        # Multiply the close price by the number of shares held, or the Position
        signals_df['PortfolioHoldings'] = signals_df['close'] * signals_df['Position']

        # Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
        signals_df['PortfolioCash'] = initial_capital - (signals_df['close'] * signals_df['TradePosition']).cumsum()

        # Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
        signals_df['PortfolioValue'] = signals_df['PortfolioCash'] + signals_df['PortfolioHoldings']

        # Calculate the portfolio daily returns
        signals_df['PortfolioDailyReturns'] = signals_df['PortfolioValue'].pct_change()

        # Calculate the portfolio cumulative returns
        signals_df['PortfolioCumulativeReturns'] = (1 + signals_df['PortfolioDailyReturns']).cumprod() - 1

        st.write('BackTest Processing COMPLETED...')
        st.write(signals_df.head())
        st.write(signals_df.tail())

        st.write('Visualize exit position relative to total portfolio value')
        backtestexitplot = signals_df[signals_df['Entry/Exit'] == -1.0]['PortfolioValue'].hvplot.scatter(
            color='red',
            marker='v',
            legend=False,
            ylabel='Total Portfolio Value',
            width=1000,
            height=400
        )
        st.write(hv.render(backtestexitplot, backend='bokeh'))

        st.write('Visualize entry position relative to total portfolio value')
        backtestentryplot = signals_df[signals_df['Entry/Exit'] == 1.0]['PortfolioValue'].hvplot.scatter(
            color='green',
            marker='^',
            ylabel='Total Portfolio Value',
            width=1000,
            height=400
        )
        st.write(hv.render(backtestentryplot, backend='bokeh'))

        st.write('Visualize the value of the total portfolio')
        total_portfolio_value_plot = signals_df[['PortfolioValue']].hvplot.line(
            line_color='lightgray',
            ylabel='Total Portfolio Value',
            xlabel='Date',
            width=1000,
            height=400
        )
        st.write(hv.render(total_portfolio_value_plot, backend='bokeh'))

        st.write('Total Portolio Overview')
        portfolio_plot = total_portfolio_value_plot * backtestentryplot * backtestexitplot
        portfolio_plot.opts(
            title="Apple Algorithm - Total Portfolio Value",
            yformatter='%.0f'
        )
        st.write(hv.render(portfolio_plot, backend='bokeh'))

        st.write('Back Test Analysis')
        portfolio_max =  round(signals_df['PortfolioValue'].max())
        st.write(f'Maximum Portfolio Value is { portfolio_max}')
        portfolio_min = round(signals_df['PortfolioValue'].min())
        st.write(f'Minimum Portfolio Value is { portfolio_min}')
        portfolio_final = round(signals_df['PortfolioValue'].iloc[-1])
        st.write(f'Final Portfolio Value is { portfolio_final}')

        portfolio_max2 = DataFramer.GetNumericColumnMax(signals_df, 'PortfolioValue', 2)
        st.write(f'Maximum Portfolio Value is { portfolio_max2}')
        portfolio_min2 = DataFramer.GetNumericColumnMin(signals_df, 'PortfolioValue', 2)
        st.write(f'Minimum Portfolio Value is { portfolio_min2}')
        portfolio_init2 = DataFramer.GetNumericColumnFirst(signals_df, "PortfolioValue", 2)
        st.write(f'Initial Portfolio Value is { portfolio_init2}')
        portfolio_final2 = DataFramer.GetNumericColumnLast(signals_df, "PortfolioValue", 2)
        st.write(f'Final Portfolio Value is { portfolio_final2}')

        signals_Aggrid = Aggridder.GetAggrid(signals_df)
        st.table(signals_df)
        st.write('Completed Analysis')