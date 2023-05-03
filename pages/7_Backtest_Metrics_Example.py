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

st.write(' Create a list for the column name')
columns = ['Backtest']

st.write(' Create a list holding the names of the new evaluation metrics')
metrics = [
    'Annualized Return',
    'Cumulative Returns',
    'Annual Volatility',
    'Sharpe Ratio',
    'Sortino Ratio']

st.write(' Initialize the DataFrame with index set to the evaluation metrics and the column')
portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

st.write(' Review the DataFrame')
st.write(portfolio_evaluation_df)

st.write(' Calculate annualized return')
portfolio_evaluation_df.loc['Annualized Return'] = (signals_df['Portfolio Daily Returns'].mean() * 252)
st.write(portfolio_evaluation_df)

st.write('Calculate cumulative return')
portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df['Portfolio Cumulative Returns'][-1]
st.write(portfolio_evaluation_df)

st.write(' Calculate annual volatility')
portfolio_evaluation_df.loc['Annual Volatility'] = (signals_df['Portfolio Daily Returns'].std() * np.sqrt(252))
st.write(portfolio_evaluation_df)

st.write(' Calculate Sharpe ratio')
portfolio_evaluation_df.loc['Sharpe Ratio'] = (signals_df['Portfolio Daily Returns'].mean() * 252) / (signals_df['Portfolio Daily Returns'].std() * np.sqrt(252))
st.write(portfolio_evaluation_df)

st.write('Calculate downside return values')
st.write('Create a DataFrame that contains the Portfolio Daily Returns column')
sortino_ratio_df = signals_df[['Portfolio Daily Returns']].copy()

st.write(' Create a column to hold downside return values')
sortino_ratio_df.loc[:,'Downside Returns'] = 0

st.write(' Find Portfolio Daily Returns values less than 0, square those values, and add them to the Downside Returns column')
sortino_ratio_df.loc[sortino_ratio_df['Portfolio Daily Returns'] < 0, 'Downside Returns'] = sortino_ratio_df['Portfolio Daily Returns']**2

st.write('Review the DataFrame')
sortino_ratio_df.tail()

st.write('Calculate the Sortino ratio')
st.write(' Calculate the annualized return value')
annualized_return = (sortino_ratio_df['Portfolio Daily Returns'].mean() * 252)
st.write('Calculate the annualized downside standard deviation value')
downside_standard_deviation = (np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252))
st.write('The Sortino ratio is reached by dividing the annualized return value by the downside standard deviation value')
sortino_ratio = annualized_return/downside_standard_deviation
st.write('Add the Sortino ratio to the evaluation DataFrame')
portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio
st.write(portfolio_evaluation_df)


st.write('Initialize trade evaluation DataFrame with columns')
trade_evaluation_df = pd.DataFrame(
    columns=[
        'Stock',
        'Entry Date',
        'Exit Date',
        'Shares',
        'Entry Share Price',
        'Exit Share Price',
        'Entry Portfolio Holding',
        'Exit Portfolio Holding',
        'Profit/Loss']
)
st.write(' Initialize iterative variables')
entry_date = ""
exit_date = ""
entry_portfolio_holding = 0.0
exit_portfolio_holding = 0.0
share_size = 0
entry_share_price = 0.0
exit_share_price = 0.0

st.write(' Loop through signal DataFrame  If `Entry/Exit` is 1, set entry trade metrics  Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit  Then append the record to the trade evaluation DataFrame')
for index, row in signals_df.iterrows():
    if row['Entry/Exit'] == 1:
        entry_date = index
        entry_portfolio_holding = row['Portfolio Holdings']
        share_size = row['Entry/Exit Position']
        entry_share_price = row['close']

    elif row['Entry/Exit'] == -1:
        exit_date = index
        exit_portfolio_holding = abs(row['close'] * row['Entry/Exit Position'])
        exit_share_price = row['close']
        profit_loss = exit_portfolio_holding - entry_portfolio_holding
        trade_evaluation_df = trade_evaluation_df.append(
            {
                'Stock': 'AAPL',
                'Entry Date': entry_date,
                'Exit Date': exit_date,
                'Shares': share_size,
                'Entry Share Price': entry_share_price,
                'Exit Share Price': exit_share_price,
                'Entry Portfolio Holding': entry_portfolio_holding,
                'Exit Portfolio Holding': exit_portfolio_holding,
                'Profit/Loss': profit_loss
            },
            ignore_index=True)

# Print the DataFrame
trade_eval_Aggrid = Aggridder.GetAggrid(trade_evaluation_df)
trade_eval_Aggrid2 = Aggridder.GetAggrid(trade_evaluation_df, False, True)
st.write('Detailed Analysis')

TotalTrades = 0
ProfitTrades = 0
LossTrades = 0
TradeAccuracy = 0
MaxSingleTradeProfit = 0
MaxSingleTradeLoss = 0
MinSingleTradeProfit = 0
MinSingleTradeLoss = 0

st.write(f'The Trading Algorithm made {TotalTrades} trades')
st.write(f'Profitable Trades were {ProfitTrades}')
st.write(f'Unprofitable Trades were {LossTrades}')
st.write(f'Trade Accuracy (percentage of profitable trades to total trades) is {TradeAccuracy}')
st.write(f'The Maximum gain on any trade was {MaxSingleTradeProfit}')
st.write(f'The Maximum loss on any trade was {MaxSingleTradeLoss}')
st.write(f'The Minimum gain on any Trade was {MinSingleTradeProfit}')
st.write(f'The Minimum loss on any Trade wa {MinSingleTradeLoss}')