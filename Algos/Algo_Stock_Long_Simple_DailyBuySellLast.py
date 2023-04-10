# Imports
import pandas as pd
import numpy as np

def Init(dfTicker):
        # Initialize TradeType column to track buys and sells
    dfTicker["TradeType"] = np.nan

    dfTicker["Accumulated"] = np.nan

    # Initialize a CostAmount column for recording trade metrics
    dfTicker["CostAmount"] = np.nan


    # Initialize share size and accumulated Shares
    quantity = 100
    accumulated_shares = 0

    # Initialize variable to hold previous price
    previous_price = 0

    # Loop through the Pandas DataFrame and initiate a trade at each iteration 
    for index, row in dfTicker.iterrows():
        
        # buy if the previous price is 0, in other words, buy on the first day
        # set the CostAmount column equal to the negative value of the row Close price multiplied by the quantity
        if previous_price == 0:
            dfTicker.loc[index, "TradeType"] = "buy"
            dfTicker.loc[index, "CostAmount"] = round(-(row["Close"] * quantity), 2)
            accumulated_shares += quantity
            dfTicker.loc[index, "Accumulated"] = accumulated_shares

        # buy if the current day price is less than the previous day price
        # set the CostAmount column equal to the negative value of the row Close price
        # multiplied by the quantity
        elif row["Close"] < previous_price:
            dfTicker.loc[index, "TradeType"] = "buy"
            dfTicker.loc[index, "CostAmount"] = round(-(row["Close"] * quantity), 2)
            accumulated_shares += quantity
            dfTicker.loc[index, "Accumulated"] = accumulated_shares
        
        # hold if the current day price is greater than the previous day price
        elif row["Close"] > previous_price:
            dfTicker.loc[index, "TradeType"] = "hold"

        # also hold if the current day price is equal to the previous day price
        else:
            dfTicker.loc[index, "TradeType"] = "hold"
        
        # set the previous_price variable to the Close price of the current row
        previous_price = row["Close"]
        
        # if the index is the last index of the Dataframe, sell
        # set the CostAmount column equal to the row Close price multiplied 
        # by the accumulated_shares
        if index == dfTicker.index[-1]:
            if(accumulated_shares>0):
                dfTicker.loc[index, "TradeType"] = "sell"
                dfTicker.loc[index, "CostAmount"] = round(row["Close"] * accumulated_shares, 2)
                dfTicker.loc[index, "Accumulated"] = 0
            else:
                dfTicker.loc[index, "TradeType"] = "none"
                dfTicker.loc[index, "CostAmount"] = 0
                dfTicker.loc[index, "Accumulated"] = 0

    TotalProfitLoss = round(dfTicker["CostAmount"].sum(), 2)

    # Review the DataFrame
    return dfTicker, TotalProfitLoss
