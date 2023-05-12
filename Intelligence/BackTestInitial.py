import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from path import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from Intelligence import BackTestFinal, Utils
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import holoviews as hv
import numpy as np
import Intelligence.Aggridder as Aggridder

def Evaluate(dfSignals) -> pd.DataFrame:
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
    portfolio_evaluation_df.loc['Annualized Return'] = (dfSignals['Portfolio Daily Returns'].mean() * 252)
    st.write(portfolio_evaluation_df)

    st.write('Calculate cumulative return')
    portfolio_evaluation_df.loc['Cumulative Returns'] = dfSignals['Portfolio Cumulative Returns'][-1]
    st.write(portfolio_evaluation_df)

    st.write(' Calculate annual volatility')
    portfolio_evaluation_df.loc['Annual Volatility'] = (dfSignals['Portfolio Daily Returns'].std() * np.sqrt(252))
    st.write(portfolio_evaluation_df)

    st.write(' Calculate Sharpe ratio')
    portfolio_evaluation_df.loc['Sharpe Ratio'] = (dfSignals['Portfolio Daily Returns'].mean() * 252) / (dfSignals['Portfolio Daily Returns'].std() * np.sqrt(252))
    st.write(portfolio_evaluation_df)

    st.write('Calculate downside return values')
    st.write('Create a DataFrame that contains the Portfolio Daily Returns column')
    sortino_ratio_df = dfSignals[['Portfolio Daily Returns']].copy()

    st.write(' Create a column to hold downside return values')
    sortino_ratio_df.loc[:,'Downside Returns'] = 0

    st.write(' Find Portfolio Daily Returns values less than 0, square those values, and add them to the Downside Returns column')
    sortino_ratio_df.loc[sortino_ratio_df['Portfolio Daily Returns'] < 0, 'Downside Returns'] = sortino_ratio_df['Portfolio Daily Returns']**2

    st.write('Review the DataFrame')
    sortino_ratio_df.tail()

    st.write('Calculate the Sortino ratio')
    st.write(' Calculate the annualized return value')
    annualized_return = (sortino_ratio_df['Portfolio Daily Returns'].mean() * 252)
    annualized_return_percent = round(annualized_return*100,2)
    st.write('Calculate the annualized downside standard deviation value')
    downside_standard_deviation = (np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252))
    st.write('The Sortino ratio is reached by dividing the annualized return value by the downside standard deviation value')
    sortino_ratio = annualized_return/downside_standard_deviation
    st.write('Add the Sortino ratio to the evaluation DataFrame')
    portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio
    st.write(portfolio_evaluation_df)
    st.write('Evaluate the Metrics - Based on the metrics that the portfolio evaluation DataFrame contains, we can estimate the following:')
    st.write(f'Annualized return: A portfolio that this trading algorithm manages should yield an annualized return of about {annualized_return_percent}%.')
    st.write(f'That is, the dollar value of the portfolio should increase by about {annualized_return_percent}% each year.')
    cumreturns = portfolio_evaluation_df.loc['Cumulative Returns', 'Backtest']
    cumreturns_percent = round(cumreturns * 100, 2)
    st.write(f'Cumulative returns: The dollar value of the portfolio increased by approximately {cumreturns_percent}% over the backtesting period. We can reasonably expect a similar growth trajectory for the future.')
    annualized_volatility = portfolio_evaluation_df.loc['Annual Volatility', 'Backtest']
    annualized_volatility_percent = round(annualized_volatility*100,2)
    st.write(f'Annual volatility: The annual volatility of the portfolio should have a spread of about {annualized_volatility_percent}% surrounding the annualized return.')
    st.write(f'This means that the portfolio might return as much as {annualized_return_percent+annualized_volatility_percent}% ({annualized_return_percent}% + {annualized_volatility_percent}%) or lose as much as {round(annualized_return_percent-annualized_volatility_percent,2)}% ({annualized_return_percent}% - {annualized_volatility_percent}%)')
    sharpe_ratio = round(portfolio_evaluation_df.loc['Sharpe Ratio', 'Backtest'],2)
    st.write(f'Sharpe ratio: The Sharpe ratio, which evaluates the performance of a portfolio on a risk-adjusted basis, is {sharpe_ratio}.')
    st.write('In general, a higher Sharpe ratio indicates a better risk/reward profile. We commonly get a Sharpe ratio of about 1.00 for a portfolio with a favorable risk-adjusted profile. However, a single Sharpe ratio doesn’t offer much insight.')
    st.write('It’s best to compare it with the Sharpe ratios of other portfolios to determine which one offers the best profile.')
    st.write(f'Sortino ratio: The Sortino ratio of our portfolio suggests a rate of about {round(sortino_ratio,2)} for the risk-adjusted annual profitability compared to the annual downside risk.')
    st.write('As with the Sharpe ratio, a higher Sortino ratio is better. And, it’s best to compare it with the Sortino ratios of other portfolios.')
    return portfolio_evaluation_df