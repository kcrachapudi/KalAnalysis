import pandas as pd
import yfinance as yf

def GetTickersData(lstTickers):
    return GetYFinanceData(lstTickers)

def GetYFinanceData2(lstTickers):
    DataFrame: df_Data
    #data = yf.download(tickers[0], start="2017-01-01", end="2017-04-30")

    df_Data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = lstTickers,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = "5y",

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = "1d",

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            #auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            #prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            #threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            #proxy = None
        )
    #Filter Out Other Columns and return only 'Close'
    #df_Data = df_Data[['Close']]
    return df_Data


def GetYFinanceData(lstTickers):
    DataFrame: df_Data
    #data = yf.download(tickers[0], start="2017-01-01", end="2017-04-30")

    df_Data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = lstTickers,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = "5y",

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = "1d",

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            #auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            #prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            #threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            #proxy = None
        )
    #Filter Out Other Columns and return only 'Close'
    #df_Data = df_Data[['Close']]
    return df_Data