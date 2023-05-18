import array
import pandas as pd
import numpy as np
import datetime
import traceback
import array

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

def GetProcessedArrayFromArray(originalArray, func, lstFuncArgs):
    newArray:array
    lstArr = []
    if(originalArray is None):
        newArray = originalArray
    else:
        for val in originalArray:
            lstArr.append(func(val, lstFuncArgs[0], lstFuncArgs[1], lstFuncArgs[2]))
        newArray = array.array('i', lstArr)        
    return newArray


def CompareAndReturnInt(originalVal:str, compareVal:str, matchReturnVal:int, elseReturnVal:int):
    intVal:int
    if(originalVal==compareVal):
        intVal = matchReturnVal
    else:
        intVal = elseReturnVal
    return intVal
