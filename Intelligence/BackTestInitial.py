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
import Aggridder

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
    st.write('Calculate the annualized downside standard deviation value')
    downside_standard_deviation = (np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252))
    st.write('The Sortino ratio is reached by dividing the annualized return value by the downside standard deviation value')
    sortino_ratio = annualized_return/downside_standard_deviation
    st.write('Add the Sortino ratio to the evaluation DataFrame')
    portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio
    st.write(portfolio_evaluation_df)
    return portfolio_evaluation_df