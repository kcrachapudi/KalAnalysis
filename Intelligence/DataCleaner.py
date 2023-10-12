import imp
import pandas as pd
from pathlib import Path
import numpy as np
import datetime
import traceback
import numbers


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
