import pandas as pd
import numpy as np
import datetime
import traceback

# def DictionaryRenameKeys(dict, dictKeyChanges):
#     for item in dictKeyChanges:
#         for key in item:
#             if(dictKeyChanges.has_key(key)):
#                 newkey = dictKeyChanges[key]
#                 di
#                 sub[key] = sub[key]
#     return dict


def ConvertDictionaryVals(dctData, func):
    for key in dctData:
        if(isinstance(dctData[key], dict)):
            ConvertDictionaryVals(dctData=dctData[key], func=func)
        else:
            dctData[key] = func(dctData[key])            
    return dctData

def Round3(original):
    if(original is None):
        return original
    else:
        try:
            original = round(original, 3)
        finally:
            pass
    return original