import pandas as pd
import yfinance as yf

def GetTickersData(lstTickers, timeperiod='1mo'):
    return GetYFinanceData(lstTickers, timeperiod)

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


def GetYFinanceData(lstTickers, timeperiod):
    DataFrame: df_Data
    #data = yf.download(tickers[0], start="2017-01-01", end="2017-04-30")

    df_Data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = lstTickers,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = timeperiod,
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


def GetYFTickerHistory(ticker, historyperiod='1y'):
    tickerdata = yf.Ticker(ticker=ticker)
    # get historical market data
    hist = tickerdata.history(period=historyperiod)
    return hist


def GetYFTickerAllData(ticker, historyperiod='1y'):
    tickerdata = yf.Ticker(ticker=ticker)

    # get historical market data
    hist = tickerdata.history(period=historyperiod)

    # get all stock info
    tickerdata.info

    # show meta information about the history (requires history() to be called first)
    tickerdata.history_metadata

    # show actions (dividends, splits, capital gains)
    tickerdata.actions
    tickerdata.dividends
    tickerdata.splits
    tickerdata.capital_gains  # only for mutual funds & etfs

    # show share count
    # - yearly summary:
    tickerdata.shares
    # - accurate time-series count:
    tickerdata.get_shares_full(start="2022-01-01", end=None)

    # show financials:
    # - income statement
    tickerdata.income_stmt
    tickerdata.quarterly_income_stmt
    # - balance sheet
    tickerdata.balance_sheet
    tickerdata.quarterly_balance_sheet
    # - cash flow statement
    tickerdata.cashflow
    tickerdata.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    tickerdata.major_holders
    tickerdata.institutional_holders
    tickerdata.mutualfund_holders

    # show earnings
    tickerdata.earnings
    tickerdata.quarterly_earnings

    # show sustainability
    tickerdata.sustainability

    # show analysts recommendations
    tickerdata.recommendations
    tickerdata.recommendations_summary
    # show analysts other work
    tickerdata.analyst_price_target
    tickerdata.revenue_forecasts
    tickerdata.earnings_forecasts
    tickerdata.earnings_trend

    # show next event (earnings, etc)
    tickerdata.calendar

    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
    # Note: If more are needed use tickerdata.get_earnings_dates(limit=XX) with increased limit argument.
    tickerdata.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    tickerdata.isin

    # show options expirations
    tickerdata.options

    # show news
    tickerdata.news

    # get option chain for specific expiration
    opt = tickerdata.option_chain('YYYY-MM-DD')
    # data available via: opt.calls, opt.puts