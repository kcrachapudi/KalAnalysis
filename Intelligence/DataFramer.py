import imp
import pandas as pd
from pathlib import Path
import numpy as np
import datetime
import traceback
import numbers
from decimal import Decimal

def SetDataFrameColsTo2Decimals(dfData:pd.DataFrame, lstcols:list):
    for col in lstcols:
        dfData[col] = dfData[col].map('{:,.2f}'.format)
    return dfData


def SetDataFrameColsToCurrency(dfData:pd.DataFrame, lstcols:list):
    for col in lstcols:
        dfData[col] = dfData[col].map('${:,.2f}'.format)
    return dfData


def GetNumericColumnMax(dfData, colName, roundNum=-1):
    value = 0.0
    try:
        if(dfData is not None):
            value = dfData[colName].max()     
            if(roundNum != -1 and isinstance(value, numbers.Number)):
                value =  round(value, roundNum)                
    except Exception as ex:
        pass
    return value

def GetNumericColumnMin(dfData, colName, roundNum=-1):
    value = 0.0
    try:
        if(dfData is not None):
            value = dfData[colName].min()        
            if(roundNum != -1 and isinstance(value, numbers.Number)):
                value =  round(value, roundNum)                
    except Exception as ex:
        pass
    return value

def GetNumericColumnFirst(dfData, colName, roundNum=-1):
    value = 0.0
    try:
        if(dfData is not None):
            value = dfData[colName].iloc[0]        
            if(roundNum != -1 and isinstance(value, numbers.Number)):
                value =  round(value, roundNum)                
    except Exception as ex:
        pass
    return value

def GetNumericColumnLast(dfData, colName, roundNum=-1):
    value = 0.0
    try:
        if(dfData is not None):
            value = dfData[colName].iloc[-1]        
            if(roundNum != -1 and isinstance(value, numbers.Number)):
                value = round(value, roundNum)                
    except Exception as ex:
        pass
    return value
