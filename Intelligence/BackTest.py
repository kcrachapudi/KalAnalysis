import imp
import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from path import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import holoviews as hv
import numpy as np
import DataFramer
from Intelligence import *

class BackTest:

        def __init__(self,dfData, initCapital, shareSize):               
            # Set initial capital
            initial_capital = float(100000)
            st.write(f'Initial Capital is {initial_capital}')
            # Set the share size
            share_size = 500
            st.write(f'ShareSize is {share_size}')
            st.write('BackTest Processing of Algorithm...')
            # Buy a 500 share position when the dual moving average crossover Signal equals 1 (SMA50 is greater than SMA100)
            # Sell a 500 share position when the dual moving average crossover Signal equals 0 (SMA50 is less than SMA100)
            dfData['Position'] = share_size * dfData['Signal']

            # Determine the points in time where a 500 share position is bought or sold
            dfData['TradePosition'] = dfData['Position'].diff()

            # Multiply the close price by the number of shares held, or the Position
            dfData['PortfolioHoldings'] = dfData['close'] * dfData['Position']

            # Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
            dfData['PortfolioCash'] = initial_capital - (dfData['close'] * dfData['TradePosition']).cumsum()

            # Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
            dfData['PortfolioValue'] = dfData['PortfolioCash'] + dfData['PortfolioHoldings']

            # Calculate the portfolio daily returns
            dfData['PortfolioDailyReturns'] = dfData['PortfolioValue'].pct_change()

            # Calculate the portfolio cumulative returns
            dfData['PortfolioCumulativeReturns'] = (1 + dfData['PortfolioDailyReturns']).cumprod() - 1

            st.write('BackTest Processing COMPLETED...')
            st.write(dfData.head())
            st.write(dfData.tail())

            st.write('Visualize exit position relative to total portfolio value')
            backtestexitplot = dfData[dfData['Entry/Exit'] == -1.0]['PortfolioValue'].hvplot.scatter(
                color='red',
                marker='v',
                legend=False,
                ylabel='Total Portfolio Value',
                width=1000,
                height=400
            )
            st.write(hv.render(backtestexitplot, backend='bokeh'))

            st.write('Visualize entry position relative to total portfolio value')
            backtestentryplot = dfData[dfData['Entry/Exit'] == 1.0]['PortfolioValue'].hvplot.scatter(
                color='green',
                marker='^',
                ylabel='Total Portfolio Value',
                width=1000,
                height=400
            )
            st.write(hv.render(backtestentryplot, backend='bokeh'))

            st.write('Visualize the value of the total portfolio')
            total_portfolio_value_plot = dfData[['PortfolioValue']].hvplot.line(
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
            portfolio_max = DataFramer.GetNumericColumnMax(dfData, 'PortfolioValue', 2)
            st.write(f'Maximum Portfolio Value is { portfolio_max}')
            portfolio_min = DataFramer.GetNumericColumnMin(dfData, 'PortfolioValue', 2)
            st.write(f'Minimum Portfolio Value is { portfolio_min}')
            portfolio_init = DataFramer.GetNumericColumnFirst(dfData, "PortfolioValue", 2)
            st.write(f'Initial Portfolio Value is { initial_capital}')
            portfolio_final = DataFramer.GetNumericColumnLast(dfData, "PortfolioValue", 2)
            st.write(f'Final Portfolio Value is { portfolio_final}')

            profit_loss = portfolio_final - initial_capital
            st.write(f'Profit/Loss is { profit_loss}')

            # Extract column values by using DataFrame.loc[] property.
            dfBuys=dfData.loc[dfData['TradePosition'] == 500, 'close']
            buyDates = dfBuys.index
            buyDates2 = buyDates.strftime('%Y-%m-%d').tolist()
            st.write(f'Buy Dates are {buyDates2}')
            
            
            dfSells=dfData.loc[dfData['TradePosition'] == -500, 'close']
            sellDates = dfSells.index
            sellDates2 = sellDates.strftime('%Y-%m-%d').tolist()
            st.write(f'Sell Dates are {sellDates2}')
        