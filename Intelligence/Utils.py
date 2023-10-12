import imp
import pandas as pd
from pathlib import Path
import numpy as np
import datetime
import traceback


def get_download_details():
    download_date = None
    try:
        absdir = Path(__file__).parent.absolute()
        csvreadname = 'download_details.csv'
        csvreadpath = Path(f'{absdir}/TickerData/{csvreadname}')
        dfData = pd.read_csv(csvreadpath)
        strdownload_date = dfData.at[dfData.index[0], 'DownloadDate']
        download_date = datetime.datetime.strptime(strdownload_date , '%Y-%m-%d').date()
    except Exception as ex:
        print(f'Error in getting Download date {ex}')            
    return download_date

def GetCSVDataFromResources(fileName, indexCol) -> pd.DataFrame:
    dfData:pd.DataFrame = pd.DataFrame()
    try:
        absdir = Path(__file__).parent.absolute()
        csvreadpath = Path(f'{absdir}/../Resources/{fileName}')
        dfData = pd.read_csv(Path(csvreadpath), index_col=indexCol, parse_dates=True, infer_datetime_format=True)
    except Exception as ex:
        print(f'Error in getting csv data for {fileName} . Error is {ex}')      
        traceback.print_exc()      
    return dfData


def GetLocalTickerData(ticker, location)->pd.DataFrame:
    dfTickerData:pd.DataFrame
    try:
        csvreadname = ticker + '.csv'
        if(location is None):
            absdir = Path(__file__).parent.parent.absolute()
            csvreadpath = Path(f'{absdir}/TickerData/{csvreadname}')
        else:
            csvreadpath = Path(f'{location}/{csvreadname}')
        dfTickerData = pd.read_csv(Path(csvreadpath), index_col='Date', parse_dates=True, infer_datetime_format=True)
    except Exception as ex:
        print(f'Error in getting ticker close data for ticker {ticker}. Error is {ex}')      
        traceback.print_exc()      
    return dfTickerData


def save_dataframe_to_abslocation(dfData, filename):
    absdir = Path(__file__).parent.absolute()
    csvwritepath = Path(f'{absdir}/{filename}')
    dfData.to_csv(csvwritepath) 


def save_download_details():
    absdir = Path(__file__).parent.absolute()
    csvwritename = 'download_details.csv'
    csvwritepath = Path(f'{absdir}/TickerData/{csvwritename}')
    # initialize list of lists
    listdata = [[datetime.date.today()]]
    #Create the pandas DataFrame
    dfNow = pd.DataFrame(listdata, columns=['DownloadDate'])
    dfNow.to_csv(csvwritepath) 


def SaveTickerData(ticker, dfTicker, location):
    csvwritename = ticker +'.csv'
    if(location is None):
        absdir = Path(__file__).parent.parent.absolute()
        csvwritepath = Path(f'{absdir}/TickerData/{csvwritename}')
    else:
        csvwritepath = Path(f'{location}/{csvwritename}')
    dfTicker.to_csv(csvwritepath) 


def generate_daily_return(ticker):
    df_Temp = pd.DataFrame()
    csvreadpath = None
    csvwritepath = None
    csvreadname = None
    csvwritename = None
    absdir = Path(__file__).parent.absolute()
    csvreadname = ticker + '_Daily_Close.csv'
    #print(f'Processing {csvreadname}')
    csvreadpath = Path(f'{absdir}/Daily_Close/{csvreadname}')
    df_Temp = pd.read_csv(Path(csvreadpath), index_col='Date', parse_dates=True, infer_datetime_format=True)
    #print(df_Temp)
    df_daily_returns = df_Temp.pct_change()
    df_daily_returns.dropna(inplace=True)
    #print(df_daily_returns)
    csvwritename = ticker +'_Daily_Returns.csv'
    csvwritepath = Path(f'{absdir}/Daily_Returns/{csvwritename}')
    df_daily_returns.rename(columns = {ticker:'Daily_Return'}, inplace = True)
    df_daily_returns.to_csv(csvwritepath) 


def generate_sharpe_ratios(dfTickers, numYears):
    for ticker in dfTickers['Symbol'].tolist():
        sharpe_data = generate_ticker_sharpe_ratio(ticker, numYears)            
        dfTickers.loc[dfTickers['Symbol'] == ticker, 'AverageAnnualReturn'] = sharpe_data[0]
        dfTickers.loc[dfTickers['Symbol'] == ticker, 'AnnualStandardDeviation'] = sharpe_data[1]
        dfTickers.loc[dfTickers['Symbol'] == ticker, 'Annual_Return'] = ConvertFloatToNumString(sharpe_data[0])
        dfTickers.loc[dfTickers['Symbol'] == ticker, 'Risk_Profile'] = ConvertFloatToNumString(sharpe_data[1])
        dfTickers.loc[dfTickers['Symbol'] == ticker, 'SharpeRatio'] = sharpe_data[2]
    dfTickers.sort_values('AnnualStandardDeviation', inplace=True)
    return dfTickers
        

def generate_ticker_sharpe_ratio(ticker, numYears):
    # Using the read_csv function and the Path module, read in the "_Daily_Retruns.csv" file from the Resources folder
    # Set the "Date" as the index column
    # Be sure to set the DatetimeIndex using the parse_dates and infer_datetime_format parameters
    tickerFile = ticker +'_Daily_Returns.csv'
    absdir = Path(__file__).parent.absolute()
    tickercsvreadpath = Path(f'{absdir}/Daily_Returns/{tickerFile}')
    dfTicker = pd.read_csv(
        tickercsvreadpath, 
        index_col="Date", 
        parse_dates=True, 
        infer_datetime_format=True
    )

    # Generate summary statistics daily returns DataFrame using the Pandas describe function
    #dfTicker.describe()
    # The number of trading days is set to 252 for use throughout these calculations
    trading_days = 252

    # Calculate the annual average daily returns
    # Use the Pandas mean function to calculate the average daily return for 
    # Then multiply that value by the number of trading days in a year, using the trading_days variable set above 
    annual_average_returns = dfTicker.mean() * trading_days

    # Sort the annual average returns from lowest to highest
    annual_average_returns.sort_values()

    # Calculate the annualized standard deviation
    # Use the Pandas std function to calculate the standard deviation
    # Multiply the standard deviation by the square root (using the NumPy sqrt function) of the number of trading days
    annual_standard_deviation = dfTicker.std() * np.sqrt(trading_days)

    # Sort the annual standard deviations from lowest to highest
    annual_standard_deviation.sort_values()

    #Calculate Sharpe ratio by dividing the annual average return
    # by the annual standard deviation
    sharpe_ratios = annual_average_returns / annual_standard_deviation

    # Sort the Sharpe ratio from lowest to highest
    sharpe_ratios.sort_values()

    return annual_average_returns[0], annual_standard_deviation[0], sharpe_ratios[0]


def GetStringFromList(lstStrings):
    strFinal = ""
    if(lstStrings is not None and len(lstStrings)>0):
        for str in lstStrings:
            strFinal += str + ","
        strFinal.removesuffix(",")
    return strFinal

def ConvertFloatToNumString(num):
    ret = 0.0
    try:
        ret = f'{round(num*100,2)}%'
    except:
        pass
    return ret