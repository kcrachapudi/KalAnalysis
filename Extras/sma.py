# Initial imports
import os
import numpy as np
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import yfinance as yf

import hvplot.pandas

class SMA:
    #This class is to model the Baseline Algorithmic Trading Strategy 
    ticker = ''
    capital = 0
    short_window = 0
    long_window = 0

    total_trades = 0
    gain_trades = 0
    loss_trades = 0 
    max_profit_trade = 0
    max_loss_trade = 0
    totalTradeProfitLoss = 0
    total_portfolio_value = 0 
    finalProfitLoss = 0
    finalInvestmentValue = 0

    def __init__(self, symbol, dfSymbol, initcapital, swindow, lwindow):
        # This method is the main entry point for this class
        # All the logic in this class flows from this method
        #Initialize the variables from the input variables provided in the parameters list
        self.ticker = symbol
        self.capital = initcapital
        self.short_window = swindow
        self.long_window  = lwindow

        print(f'*********************************************************************************************************************************')

        # Call the Baseline SMA Analysis method and pass in the Ticker dataframe
        # The SMA Analysis returns back a dataframe dfSignal
        dfSignal = self.SMAAnalysis(dfSymbol)
        #print('Printing Signal Metrics of SMA Analysis')
        #print(dfSignal.tail())
        # Backtest the methodology by providing the dataframe from the SMA analysis to the BackTest method
        dfEvaluation = self.BackTest(dfSignal)
        #print('Printing Evaluation Metrics of SMA Analysis')
        #print(dfEvaluation)

        #Gather all the metrics from the Backtested results dataframe
        self.total_trades = dfEvaluation.shape[0]
        self.gain_trades = len(dfEvaluation[dfEvaluation['Profit/Loss']>0])
        self.loss_trades = len(dfEvaluation[dfEvaluation['Profit/Loss']<0])
        self.max_profit_trade = dfEvaluation.loc[dfEvaluation['Profit/Loss']>0, ['Profit/Loss']].max()
        self.max_loss_trade = dfEvaluation.loc[dfEvaluation['Profit/Loss']<0, ['Profit/Loss']].min()
        self.totalTradeProfitLoss = dfEvaluation['Profit/Loss'].sum()
        self.total_portfolio_value = dfSignal['Portfolio Total'].iloc[-1]
        self.finalInvestmentValue = self.capital + self.totalTradeProfitLoss

        #Summarize the Results of the Analysis
        self.Summary()

        print(f'---------------------------------------------------------------------------------------------------------------------------')


    def SMAAnalysis(self, dfSignal):
        #Implement the Baseline Trading Algorithm

        # Generate the short and long moving averages (50 and 100 days, respectively)
        dfSignal['SMAsmall'] = dfSignal['Close'].rolling(window=self.short_window).mean()
        dfSignal['SMAlong'] = dfSignal['Close'].rolling(window=self.long_window).mean()
        dfSignal['Signal'] = 0.0

        # Generate the trading signal 0 or 1,
        # where 1 is when the SMAsmall is less than the SMAlong
        # where 0 is when the SMAsmall is greater than than the SMAlong
        dfSignal['Signal'][self.long_window:] = np.where(
            dfSignal['SMAsmall'][self.long_window:] < dfSignal['SMAlong'][self.long_window:], 1.0, 0.0
        )

        # Calculate the points in time at which a position should be taken, 1 or -1
        dfSignal['Entry/Exit'] = dfSignal['Signal'].diff()

        #print('Milestone 1')

        # Visualize entry positions relative to close price
        exit = dfSignal[dfSignal['Entry/Exit'] == 1.0]['Close'].hvplot.scatter(
            color='purple',
            marker='^',
            legend=False,
            ylabel='Price in $',
            width=1000,
            height=400)

        # Visualize exit positions relative to close price
        entry = dfSignal[dfSignal['Entry/Exit'] == -1.0]['Close'].hvplot.scatter(
            color='orange',
            marker='v',
            legend=False,
            ylabel='Price in $',
            width=1000,
            height=400)

        # Visualize the close price for the investment
        security_close = dfSignal[['Close']].hvplot(
            line_color='lightgray',
            ylabel='Price in $',
            width=1000,
            height=400)

        # Visualize the moving averages
        moving_avgs = dfSignal[['SMAsmall', 'SMAlong']].hvplot(
            ylabel='Price in $',
            width=1000,
            height=400)

        # Overlay the plots
        entry_exit_plot = security_close * moving_avgs * entry * exit
        entry_exit_plot.opts(
            title="Stock - Long Position Dual Moving Average Trading Algorithm"
        )
        #print('Milestone 2')

        # Set the initial_capital to 100000
        initial_capital = self.capital

        # Set the share_size to 500
        # In a short-position strategy, shares are sold before they are bought 
        share_size = 500

        # Create a column named "Position" by multiplying the share_size by the Signal
        # Sell a position (-500 shares) when the dual moving average crossover Signal equals 1 (SMA50 is less than SMA100)
        # Buy a position (500 shares) when the dual moving average crossover Signal equals 0 (SMA50 is greater than SMA100)
        dfSignal["Position"] = share_size * dfSignal["Signal"]

        # Find the points in time where a 500 share position is bought or sold
        dfSignal["Entry/Exit Position"] = dfSignal["Position"].diff()

        # Create a Portfolio Holdings column by multiplying the Close price by the Position
        dfSignal["Portfolio Holdings"] = dfSignal["Close"] * dfSignal["Position"]

        # To calculate Portfolio Cash, subtract the cumulative sum of the trade cost/proceeds from the initial_capital
        # The trade cost proceeds are calculated by multiplying the Close price by Entry/Exit Position
        dfSignal["Portfolio Cash"] = (
            initial_capital - (dfSignal["Close"] * dfSignal["Entry/Exit Position"]).cumsum()
        )

        #print('Milestone 3')
        
        # Calculate the Portfolio Total value by adding Portfolio Cash and Portfolio Holdings 
        dfSignal["Portfolio Total"] = dfSignal["Portfolio Cash"] + dfSignal["Portfolio Holdings"]

        # Calculate the Portfolio Daily Returns based on the Portfolio Total
        dfSignal["Portfolio Daily Returns"] = dfSignal["Portfolio Total"].pct_change()
      
        #print('Milestone 4')
        
        # Calculate the Portfolio Cumulative Returns based on the Portfolio Daily Returns
        dfSignal["Portfolio Cumulative Returns"] = (
            1 + dfSignal["Portfolio Daily Returns"]
        ).cumprod() - 1

        #print('Milestone 5')
        
        # Visualize the entry positions relative to the Portfolio Total
        entry = dfSignal[dfSignal["Entry/Exit"] == 1.0]["Portfolio Total"].hvplot.scatter(
            color='purple',
            marker='^',
            legend=False, 
            ylabel="Total Portfolio Value", 
            width=1000, 
            height=400
        )

        # Visualize the exit positions relative to the Portfolio Total
        exit = dfSignal[dfSignal["Entry/Exit"] == -1.0]["Portfolio Total"].hvplot.scatter(
            color='orange',
            marker='v',
            legend=False, 
            ylabel="Total Portfolio Value", 
            width=1000, 
            height=400
        )

        # Visualize Portfolio Total for the investment
        total_portfolio_value = dfSignal[["Portfolio Total"]].hvplot(
            line_color="lightgray", 
            ylabel="Total Portfolio Value", 
            width=1000, 
            height=400
        )

        # Overlay the entry, exit and total_portfolio_value plots
        portfolio_entry_exit_plot = total_portfolio_value * entry * exit
        portfolio_entry_exit_plot.opts(
            title="VAQ Short-Position Algorithm - Total Portfolio Value",
            yformatter='%.0f'
        )
        #print('Milestone 6')
        return dfSignal


    def BackTest(self, dfSignal):
        # Create a list for the column name
        columns = ['Backtest']

        # Create a list holding the names of the new evaluation metrics
        metrics = [
            'Annualized Return',
            'Cumulative Returns',
            'Annual Volatility',
            'Sharpe Ratio',
            'Sortino Ratio']

        # Initialize the DataFrame with index set to the evaluation metrics and the column
        portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

        # Calculate annualized return
        portfolio_evaluation_df.loc['Annualized Return'] = (
            dfSignal['Portfolio Daily Returns'].mean() * 252
        )

        # Calculate cumulative return
        portfolio_evaluation_df.loc['Cumulative Returns'] = dfSignal['Portfolio Cumulative Returns'][-1]
        
        # Calculate annual volatility
        portfolio_evaluation_df.loc['Annual Volatility'] = (
            dfSignal['Portfolio Daily Returns'].std() * np.sqrt(252)
        )

        # Calculate Sharpe ratio
        portfolio_evaluation_df.loc['Sharpe Ratio'] = (
            dfSignal['Portfolio Daily Returns'].mean() * 252) / (
            dfSignal['Portfolio Daily Returns'].std() * np.sqrt(252)
        )

        # Calculate downside return values

        # Create a DataFrame that contains the Portfolio Daily Returns column
        sortino_ratio_df = dfSignal[['Portfolio Daily Returns']].copy()

        # Create a column to hold downside return values
        sortino_ratio_df.loc[:,'Downside Returns'] = 0

        # Find Portfolio Daily Returns values less than 0,
        # square those values, and add them to the Downside Returns column
        sortino_ratio_df.loc[sortino_ratio_df['Portfolio Daily Returns'] < 0,
                            'Downside Returns'] = sortino_ratio_df['Portfolio Daily Returns']**2

        # Review the DataFrame
        sortino_ratio_df.tail()

        # Calculate the Sortino ratio

        # Calculate the annualized return value
        annualized_return = (
            sortino_ratio_df['Portfolio Daily Returns'].mean() * 252
        )

        # Calculate the annualized downside standard deviation value
        downside_standard_deviation = (
            np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252)
        )

        # The Sortino ratio is reached by dividing the annualized return value
        # by the downside standard deviation value
        sortino_ratio = annualized_return/downside_standard_deviation

        # Add the Sortino ratio to the evaluation DataFrame
        portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio


        # Initialize trade evaluation DataFrame with columns
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

        # Initialize iterative variables
        entry_date = ""
        exit_date = ""
        entry_portfolio_holding = 0.0
        exit_portfolio_holding = 0.0
        share_size = 0
        entry_share_price = 0.0
        exit_share_price = 0.0

        # Loop through signal DataFrame
        # If `Entry/Exit` is 1, set entry trade metrics
        # Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit
        # Then append the record to the trade evaluation DataFrame
        for index, row in dfSignal.iterrows():
            if row['Entry/Exit'] == 1:
                entry_date = index
                entry_portfolio_holding = row['Portfolio Holdings']
                share_size = row['Entry/Exit Position']
                entry_share_price = row['Close']

            elif row['Entry/Exit'] == -1:
                exit_date = index
                exit_portfolio_holding = abs(row['Close'] * row['Entry/Exit Position'])
                exit_share_price = row['Close']
                profit_loss = exit_portfolio_holding - entry_portfolio_holding
                trade_evaluation_df = trade_evaluation_df.append(
                    {
                        'Stock': self.ticker,
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

        return trade_evaluation_df


    def Summary(self):
        print(f'Analysis Summary for {self.ticker}')
        print(f'Analysis Type: Simple Moving Average Crossover({self.short_window}, {self.long_window}) ')
        print(f'Initial Capital: ${round(self.capital,2)}')
        #print(f' Total Number of Trades: {self.total_trades} ')
        #print(f' Total Number of Profitable Trades: {self.gain_trades} ')
        #print(f' Total Number of Loss Trades: {self.loss_trades} ')
        #print(f' Maximum Profitable Trade: {self.max_profit_trade} ')
        #print(f' Maximum Loss Trade: {self.max_loss_trade} ')
        print(f'Total Trade Profit/Loss: {round(self.totalTradeProfitLoss, 2)} ')
        #print(f'Total Portfolio Value: {self.total_portfolio_value}')
        print(f'Final Investment Value : {round(self.finalInvestmentValue, 2)}')