# Import the required libraries and dependencies
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import holoviews as hv
import numpy as np
import Aggridder

def Evaluate(dfData):
    st.write('Initialize trade evaluation DataFrame with columns')
    dfTradeEvaluator:pd.DataFrame = pd.DataFrame(
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
    for index, row in dfData.iterrows():
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
            dfTradeEvaluator = dfTradeEvaluator.append(
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
    st.write(dfTradeEvaluator)
    #trade_eval_Aggrid = Aggridder.GetAggrid(dfTradeEvaluator)
    #rade_eval_Aggrid2 = Aggridder.GetAggrid(dfTradeEvaluator, True, True)
    st.write('Detailed Analysis')

    TotalTrades:int = dfTradeEvaluator.shape[0]
    ProfitTrades:int = (dfTradeEvaluator['Profit/Loss'] > 0).sum()
    LossTrades:int = (dfTradeEvaluator['Profit/Loss'] < 0).sum()
    TradeAccuracy = (ProfitTrades/TotalTrades)*100
    MaxSingleTradeProfit = dfTradeEvaluator['Profit/Loss'].max()
    MaxSingleTradeLoss = dfTradeEvaluator['Profit/Loss'].min()
    dfProfits = dfTradeEvaluator.loc[dfTradeEvaluator['Profit/Loss']>0]
    st.write(dfProfits)
    dfLosses = dfTradeEvaluator.loc[dfTradeEvaluator['Profit/Loss']<0]
    st.write(dfLosses)

    MinSingleTradeProfit = dfProfits.iloc[:,8].min()
    MinSingleTradeLoss = dfLosses.iloc[:,8].max()

    st.write(f'The Trading Algorithm made {TotalTrades} trades')
    st.write(f'Profitable Trades were {ProfitTrades}')
    st.write(f'Unprofitable Trades were {LossTrades}')
    st.write(f'Trade Accuracy (percentage of profitable trades to total trades) is {TradeAccuracy}')
    st.write(f'The Maximum gain on any trade was {MaxSingleTradeProfit}')
    st.write(f'The Maximum loss on any trade was {MaxSingleTradeLoss}')
    st.write(f'The Minimum gain on any Trade was {MinSingleTradeProfit}')
    st.write(f'The Minimum loss on any Trade wa {MinSingleTradeLoss}')