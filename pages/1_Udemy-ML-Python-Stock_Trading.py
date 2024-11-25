import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import date, time
#Install Yahoo Finance Libraries
import yfinance as yf
import yahoofinancials as YahooFinancials
from StreamlitExtras import StreamlitControls as stc
import plotly.express as px
import warnings
import numpy as np
import pandas_ta as ta
warnings.filterwarnings('ignore')

st.session_state.ticker = st.sidebar.text_input("Enter the Ticker")
st.session_state.startYear = st.sidebar.text_input("Enter the Start Year")


@st.cache_data
def GetTickerData(ticker, startdate, enddate):
    return yf.download(ticker, start=startdate, end=enddate, progress=False)
    
    
def DownloadAndProcessData():
    st.write(f"Stage 1 Processed! Ticker: {st.session_state.ticker}, StartYear: {st.session_state.startYear}")
    #Download Historical Data
    startdate= st.session_state.startYear + '-01-01'
    enddate=date.today()
    
    st.session_state.dfData = GetTickerData(st.session_state.ticker, startdate, enddate)
    
    st.session_state.table1 = st.empty()
    st.session_state.table2 = st.empty()
    st.session_state.chart1 = st.empty()

    stc.Container_AddDataframe(container=st.session_state.table1, dfData=st.session_state.dfData, printType='head')
    #st.write(dfData.head())
    #Remove Ticker row from Column Name
    st.session_state.dfData = st.session_state.dfData.droplevel(1, axis=1)

    # Rename the columns using the dictionary
    rename_dict = {'Close': 'close', 'Volume': 'volume', 'High':'high', 'Open':'open', 'Low':'low'}
    st.session_state.dfData.rename(columns=rename_dict, inplace=True)

    #Chart the Stock Performance
    stc.Container_AddDataframe(container=st.session_state.table2, dfData=st.session_state.dfData, printType='head')
    #st.write(dfData.head())
    #st.line_chart(dfData, y='close')
    stc.Container_AddChart(container=st.session_state.chart1, chart=px.line(st.session_state.dfData, y='close'))
    st.session_state.submitted = True
    

def CreateTAIndicatorsAndPlot():
    #Create Technical Analysis Indicators and Plot 
    if(st.session_state.dfData.empty):
        return
    
    st.session_state.table3 = st.empty()
    st.session_state.table4 = st.empty()
    st.session_state.table5 = st.empty()
    st.session_state.chart2 = st.empty()
    st.session_state.chart3 = st.empty()

    dfData = st.session_state.dfData
    # Calculate RSI
    dfData['RSI-2'] = ta.rsi(dfData['close'], length=2)
    dfData['RSI-7'] = ta.rsi(dfData['close'], length=7)
    dfData['RSI-14'] = ta.rsi(dfData['close'], length=14)
    #View Data so far
    #Chart the Stock Performance
    stc.Container_AddDataframe(container=st.session_state.table3, dfData=dfData, printType='tail')

    # Calculate CCI
    dfData['CCI-30'] = ta.cci(close=dfData['close'], length=30, high=dfData['high'], low=dfData['low'])
    dfData['CCI-50'] = ta.cci(close=dfData['close'], length=50, high=dfData['high'], low=dfData['low'])
    dfData['CCI-100'] = ta.cci(close=dfData['close'], length=100, high=dfData['high'], low=dfData['low'])
    #View Data so far
    stc.Container_AddDataframe(container=st.session_state.table4, dfData=dfData, printType='tail')
    #Drop NaN Values
    dfData.dropna()

    #View Data so far
    stc.Container_AddDataframe(container=st.session_state.table5, dfData=dfData, printType='tail')

    #Plot showing some Indicators above
    stc.Container_AddChart(container=st.session_state.chart2, chart=px.line(dfData, y='RSI-2'))
    stc.Container_AddChart(container=st.session_state.chart3, chart=px.line(dfData, y='CCI-100'))
    

def PrepareAndLabelData():
    #Prepare Data Labelling
    #What are we doing here?
    #When we place our trade: Buy at Open(over the next day). We want to close our trade: At the next day at the Open.
    #Formula: Handling the returns this way -> Buy: Open(-1)-Closing:Open(-2)
    #We want to label our data in the following day,
    #BUY SIGNAL: Open(-2)>Open(-1)
    #SELL SIGNAL: Open(-2)<Open(-1)
    #Indicators that represent our current situation, and labels take a look ahead of time to determine if we have a pattern.

    if(st.session_state.dfData.empty):
        return
        
    st.session_state.table6 = st.empty()
    
    #Prepare Data for Machine Learning
    #Create Target Column
    st.session_state.dfData['label'] = np.where(st.session_state.dfData['open'].shift(-2).gt(st.session_state.dfData['open'].shift(-1)), '1', '0')
    st.session_state.dfData.dropna(inplace=True)
    stc.Container_AddDataframe(container=st.session_state.table6, dfData=st.session_state.dfData, printType='tail')


def SetupNeuralNetwork():
    #Creating a Nueral Network
    import sklearn
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score, classification_report, confusion_matrix
    from math import sqrt

    #Fitting Indicators and Labelling
    X = st.session_state.dfData[st.session_state.dfData.columns[6:-1]].values
    y = st.session_state.dfData['label'].values

    #Split Data into Training and Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    mlp = MLPClassifier(hidden_layer_sizes=(8,8,8), activation='relu', solver='adam', max_iter=1000)
    mlp.fit(X_train, y_train)

    predict_train = mlp.predict(X_train)
    predict_test = mlp.predict(X_test)

    #Train the Model
    report_train = classification_report(y_train, predict_train)
    st.write('Train Data Report')
    st.write(report_train)

    #Test the Model
    report_test = classification_report(y_test, predict_test)
    st.write('Test Data Report')
    st.write(report_test)

    #Evaluate the Model
    #BackTesting our Model
    #Measure the returns obtained by our trading model

    st.session_state.dfData['Prediction'] = np.append(predict_train, predict_test)
    st.session_state.dfData['StrategyReturns'] = np.where(st.session_state.dfData['Prediction']=="1", st.session_state.dfData['open'].shift(-2)-st.session_state.dfData['open'].shift(-1), 0)

    st.session_state.dfData['CumulativeReturns'] = np.cumsum(st.session_state.dfData['StrategyReturns'])
    st.session_state.dfData.plot(y='CumulativeReturns')
    # Add labels
    plt.xlabel('Year')
    plt.ylabel('CumulativeReturns')
    plt.title('Cumulative Returns over Years')

    # Show the plot
    plt.show()


def ChartCumulativeReturns():
    #Chart Cumulative Returns
    st.session_state.dfData.plot(y='CumulativeReturns')
    # Add labels
    plt.xlabel('Year')
    plt.ylabel('CumulativeReturns')
    plt.title('Cumulative Returns over Years')
    # Show the plot
    plt.show()

    st.session_state.dfData['CumulativeReturns'].plot()
    # Add labels
    plt.xlabel('Year')
    plt.ylabel('CumulativeReturns')
    plt.title('Cumulative Returns over Years')
    # Show the plot
    plt.show()


def Prediction():
    prediction = st.session_state.dfData.iloc[-1]['Prediction']
    if(prediction == 1):
        st.write("Todays Return Forecast: UP")
    else:
        st.write("Todays Return Forecast: DOWN")


def StartProcess():
    DownloadAndProcessData()
    CreateTAIndicatorsAndPlot()
    PrepareAndLabelData()
    SetupNeuralNetwork()
    ChartCumulativeReturns()
    Prediction()
    
btnStartProcess = st.sidebar.button(label="Start Process", on_click=StartProcess)
