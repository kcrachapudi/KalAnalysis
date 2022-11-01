from datetime import datetime
import pandas as pd
from pathlib import Path
import numpy as np
import questionary
import cloud_data_collector
from customer import Customer
import Utils
import datetime

import matplotlib
import matplotlib_inline
from sma import SMA
from sma_ml import SMAML

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

#Setup a List of Tickers for using in our Analysis
#In future we can get this from the customer as a csv and import it instead of hardcoding
def SetupTickerDataFrame():
    lstTickers = [
        ['XLB', 'Materials'], 
        ['XLC', 'Communication Services'],
        ['XLE', 'Energy'], 
        ['XLF', 'Financials'],
        ['XLI', 'Industrials'], 
        ['XLK', 'Technology'],
        ['XLP', 'Consumer Staples'], 
        ['XLRE', 'Real Estate'],
        ['XLU', 'Utilities'], 
        ['XLV', 'HealthCare'],
        ['XLY', 'Consumer Discretionary'],
        ['SPY', 'S&P 500'],
        ['AGG', 'US Intermediate Bond Fund'],
        
        ['RIOT', 'RIOT BlockChain'],
        ['AMC', 'AMC Entertainment'],
        ['GME', 'GameStop'],
        ['GOOG', 'Google Inc'],
        ['AAPL', 'Apple Inc'],
        ['MSFT', 'Microsoft Corp'],
        ['NVDA', 'Nvidia Inc'],
        ['NKTR', 'Nektar Therapeutics'],
        ['AMD', 'Advanced Micro Devices'],
        ['M', 'Macys Inc'],
        ['GLD', 'Gold ETF']
        ]
    #Create a DataFrame with the Tickers with empty values for other columns for now
    #Once Analysis starts these columns will be populated with data
    tickercolumns = ['Symbol', 'Name']
    dfTickers = pd.DataFrame(lstTickers, columns=tickercolumns, dtype = float)
    dfTickers['AverageAnnualReturn'] = ''
    dfTickers['AnnualStandardDeviation'] = ''
    dfTickers['Annual_Return'] = ''
    dfTickers['Risk_Profile'] = ''
    dfTickers['SharpeRatio']=''
    return dfTickers


def SetupSymbolDataFrame(dfSymbol):
    if(dfSymbol is not None):
        #Create a DataFrame with empty values for other columns for now
        #Once Analysis starts these columns will be populated with data
        dfSymbol['AverageAnnualReturn'] = ''
        dfSymbol['AnnualStandardDeviation'] = ''
        dfSymbol['Annual_Return'] = ''
        dfSymbol['Risk_Profile'] = ''
        dfSymbol['SharpeRatio']=''
    return dfSymbol


def GetTickersData(lstTickers):
    #The download details from YFinance are captured and get the download date
    download_date = Utils.get_download_details()
    canDownload = False
    #Do a check to see if the data was downloaded today, if yes skip downloading again as the close prices will not change for today again
    #But if the downloaded data is stale then set the flag to can download to true
    if( isinstance(download_date, datetime.date)):
        if(download_date<datetime.date.today()):
            canDownload = True
    else:
        canDownload = True
    #If canDownload flag is true then go ahead with downloading fresh data from YFinance
    if(canDownload):
        #Download happens here
        #Provide the Tickers List to download from YFinance
        dfData = cloud_data_collector.GetTickersData(lstTickers)
        #Saving the downloaded data to CSVs happens here
        SaveTickersDownloadedData(lstTickers, dfData)
        Utils.save_download_details()
    return dfData
   

def SaveTickersDownloadedData(lstTickers, dfData):
    # Get  the Ticker Data and Save it locally for analysis
    # Saving the daily close data and generate and save daily return data as csv
    for ticker in lstTickers:
        print(dfData)
        dfTicker = dfData['Close'][ticker]
        Utils.generate_daily_close(ticker, dfTicker)
        Utils.generate_daily_return(ticker)


def gather_customer_risk_input(risk_choices):
    #Get Customer Input about their Risk Appetite
    customer = Customer()
    print("\nAbove is a basket of Securities and ETFs that are most in demand sorted by their Risk profile.\n")
    risk_profile = questionary.select(
                        "How much Risk are you willing to take?",
                        choices = list(risk_choices.keys()),
                    ).ask()
    risk_val = risk_choices[risk_profile]
    customer.cust_risk_profile = risk_profile
    customer.cust_risk_val = risk_val
    return customer

def gather_customer_investment_amount(customer):
    #Get the Amount that the Customer wants to Invest
    invalidinput = True
    while(invalidinput):
        inv_amount = questionary.text("What is the Amount you would like to Invest?").ask()
        try:
            customer.cust_inv_amount = float(inv_amount)
            if(customer.cust_inv_amount > 0):
                invalidinput = False
            else:
                print('Please enter a valid amount above zero')
        except:
            print('Invalid Amount was Input. Please try again')
    return customer


def filter_tickers_by_customer_risk_profile(dfTickers, customer):
    # Filter and return the Tickers based on the selected Customer Risk Appetite
    Customer: customer
    dfTickers["AnnualStandardDeviation"] = pd.to_numeric(dfTickers["AnnualStandardDeviation"], downcast="float")
    return dfTickers.loc[(dfTickers['AnnualStandardDeviation']*100) <= customer.cust_risk_val]

def filter_tickers_by_customer_return_profile(dfTickers, customer):
    # Filter and return the TIckers based on the selected Customer Return expectation
    Customer: customer
    dfTickers['AverageAnnualReturn'] = pd.to_numeric(dfTickers['AverageAnnualReturn'], downcast="float")
    return dfTickers.loc[(dfTickers['AverageAnnualReturn']*100) >= customer.cust_expected_return]

def gather_customer_return_input(customer):
    #Get Customer Input about their Return Expectation
    return_percent = questionary.text("What percent of Minimum Return are you expecting based on the Risk filtered Securites/ETFs? Please provide return percent as number\n. Allow atleast 3 Securities/ETFs remaining after selection.").ask()
    customer.cust_expected_return = float(return_percent)
    return customer

def gather_customer_final_ticker(customer, final_tickers):
    #Let the Customer choose one Ticker for further analysis out of the best tickers that match their Risk and Return expectations
    print("\nProceeding with Algo and ML Analysis.\n")
    final_ticker = questionary.select(
                        "Based on the Risk/Return, Sharpe Ratio details above Please Select a Symbol to proceed with further Algo and ML Analysis?",
                        choices = final_tickers
                    ).ask()
    customer.final_ticker = final_ticker
    return customer

def Init():
    #Setup the Initial Tickers list as Dataframe
    dfTickers = SetupTickerDataFrame()
    tickers = dfTickers['Symbol'].tolist()
    #The download details from YFinance are captured and get the download date
    download_date = Utils.get_download_details()
    canDownload = False
    #Do a check to see if the data was downloaded today, if yes skip downloading again as the close prices will not change for today again
    #But if the downloaded data is stale then set the flag to can download to true
    if( isinstance(download_date, datetime.date)):
        if(download_date<datetime.date.today()):
            canDownload = True
    else:
        canDownload = True
    #If canDownload flag is true then go ahead with downloading fresh data from YFinance
    if(canDownload):
        #Download happens here
        dfData = GetTickersData(tickers)
        #Saving the downloaded data to CSVs happens here
        save_etf_data(dfTickers, dfData)
        Utils.save_download_details()
    
    #Generate the metrics for the Tickers like Risk, Return and Sharpe Ratios
    dfTickers = Utils.generate_sharpe_ratios(dfTickers, numYears=5)
    dfShow = dfTickers[['Symbol', 'Name', 'Annual_Return', 'Risk_Profile', 'SharpeRatio']]
    print("\n\n\nWelcome to FinAdvisorsAI the one place to get Expert Financial Advice.")
    print(dfShow)


    risk_choices = {
        #'Minimum <5%': 5,
        'Low <25%': 25,
        'Medium <50%': 50,
        'High <75%': 75,
        'Maximum': 100000
    }

    #Customer object to save Customer Inputs
    Customer: customer

    #Gather Customer Risk Input
    customer = gather_customer_risk_input(risk_choices)

    #Filter Tickers by Customer Risk Profile
    df_Risk_Filtered = filter_tickers_by_customer_risk_profile(dfTickers, customer)
    df_Risk_Filtered.sort_values('AverageAnnualReturn', inplace=True)
    df_Risk_Filtered_Show = df_Risk_Filtered[['Symbol', 'Name', 'Annual_Return', 'Risk_Profile', 'SharpeRatio']]
    
    print(df_Risk_Filtered_Show)

    #Gather the Return Input from Customer
    invalidreturninput = True
    #As the Input can be typed we want to make sure the Input is valid and do not let them out of this question until they provide a valid answer
    while(invalidreturninput):
        try:
            customer = gather_customer_return_input(customer)
            dfData = df_Risk_Filtered.loc[(df_Risk_Filtered['AverageAnnualReturn']*100) >= customer.cust_expected_return]
            if(dfData.shape[0]>=3):
                invalidreturninput = False
        except:
            invalidreturninput = True

    #Once a valid return input is provided continue with Filtering the Tickers by the Return expectation 
    df_Return_Filtered = filter_tickers_by_customer_return_profile(df_Risk_Filtered, customer)
    df_Return_Filtered_Show = df_Return_Filtered[['Symbol', 'Name', 'Annual_Return', 'Risk_Profile', 'SharpeRatio']]

    # Make sure that atleast 3 Tickers fit in the selection criteria so that the customer can choose out of them one final ticker 
    print(df_Return_Filtered_Show)
    df_Final = pd.DataFrame()
    if(df_Return_Filtered.shape[0]>3):
        df_Final = df_Return_Filtered.tail(3)
    elif(df_Return_Filtered.shape[0]==3):
        df_Final = df_Return_Filtered

    print("Below is the final list of Securities/ETFs selected for further analysis")
    print(df_Final)
    # Gather Customer Input on the Amount they would like to Invest
    customer = gather_customer_investment_amount(customer)
    
    # At ths point we have at least 3 Tickers for the Customer to select 
    final_tickers = df_Final['Symbol'].tolist()

    # Get the Final Ticker from the Customer
    # This will be the ticker we do the Trading Algo and ML Algos on
    customer = gather_customer_final_ticker(customer, final_tickers)
    dfSymbol = Utils.get_ticker_close_data(customer.final_ticker)

    # Start FinAdvisorsAI Analysis here
    print('****************************************  Starting Algo Trading and ML Analysis ********************************************')
    shortwindow1 = 50
    longwindow1 = 200

    # Call the Basic algo for the 50-200 SMA Windows
    smaA = SMA(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow1, longwindow1)
    # Call the SVM Machine Learning algo for the 50-200 SMA Windows
    smamlA1 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow1, longwindow1, 'svm')    
    # Call the LR Machine Learning algo for the 50-200 SMA Windows
    smamlA2 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow1, longwindow1, 'lr')    
    # Call the DTC Machine Learning algo for the 50-200 SMA Windows
    smamlA3 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow1, longwindow1, 'dtc')    
    
    shortwindow2 = 10
    longwindow2 = 50

    # Call the Basic algo for the 10-50 SMA Windows
    smaB = SMA(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow2, longwindow2)
    # Call the SVM Machine Learning algo for the 10-50 SMA Windows
    smamlB1 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow2, longwindow2, 'svm')    
    # Call the LR Machine Learning algo for the 10-50 SMA Windows
    smamlB2 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow2, longwindow2, 'lr')    
    # Call the DTC Machine Learning algo for the 10-50 SMA Windows
    smamlB3 = SMAML(customer.final_ticker, dfSymbol, customer.cust_inv_amount, shortwindow2, longwindow2, 'dtc')    

