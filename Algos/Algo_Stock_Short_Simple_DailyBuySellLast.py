# Imports
import pandas as pd
import numpy as np

def Init(dfTicker):
    # Initialize TradeType column to track buys and sells
    dfTicker["TradeType"] = np.nan

    dfTicker["Accumulated"] = 0

    # Initialize a CostProceeds column for recording trade metrics
    dfTicker["CostProceeds"] = 0


    # Initialize share size and accumulated Accumulated
    quantity = 100
    accumulated_shares = 0

    # Initialize variable to Hold previous price
    previous_price = 0  

    # Loop through the Pandas DataFrame and initiate a trade at each iteration 
    for index, row in dfTicker.iterrows():        
        # initiate the trade with a short sale on the first day
        if previous_price == 0:
            dfTicker.loc[index, "TradeType"] = "SellShort"
            dfTicker.loc[index, "CostProceeds"] = -(row["Close"] * quantity)
            accumulated_shares += quantity
            dfTicker.loc[index, "Accumulated"] = accumulated_shares   
        # Hold if the current day's price is less than the previous day's price
        elif row["Close"] < previous_price:
            dfTicker.loc[index, "TradeType"] = "Hold"
            dfTicker.loc[index, "CostProceeds"] = 0
        # sell short if the current day's price is greater than the previous day's price
        elif row["Close"] > previous_price:
            dfTicker.loc[index, "TradeType"] = "SellShort"
            dfTicker.loc[index, "CostProceeds"] = -(row["Close"] * quantity)
            accumulated_shares += quantity
            dfTicker.loc[index, "Accumulated"] = accumulated_shares
        # Hold if the current day's price is equal to the previous day's price
        else:
            dfTicker.loc[index, "TradeType"] = "Hold"
        # update the previous_price to the current row's price
        previous_price = row["Close"]
        # if the index is the last index of the DataFrame, Close the position
        if index == dfTicker.index[-1]:
            dfTicker.loc[index, "TradeType"] = "ClosePosition"
            if accumulated_shares > 0:
                dfTicker.loc[index, "CostProceeds"] = row["Close"] * accumulated_shares
                dfTicker.loc[index, "Accumulated"] = 0

        TotalProfitLoss = round(dfTicker["CostProceeds"].sum(), 2)

        # Initialize the variable to Hold the value of the invested capital
        InvestedCapital = 0
        # Calculate the invested capital by adding the cost of all buy trades
        for index, row in dfTicker.iterrows():
            if row["TradeType"] == "ClosePosition":
                InvestedCapital = InvestedCapital + row["CostProceeds"]
        InvestedCapital = -(InvestedCapital)

        # Calculate the return on investment (ROI)
        ROI = round((TotalProfitLoss / -(InvestedCapital)) * 100, 2)

    return dfTicker, TotalProfitLoss, InvestedCapital, ROI

