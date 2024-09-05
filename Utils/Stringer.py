import base64

def sanitize_string(s:str):
    """Removes non-UTF-8 characters from a string."""
    return s.encode('utf-8', 'ignore').decode('utf-8')


def CompareAndReturnInt(originalVal:str, compareVal:str, matchReturnVal:int, elseReturnVal:int):
    intVal:int
    if(originalVal==compareVal):
        intVal = matchReturnVal
    else:
        intVal = elseReturnVal
    return intVal


def GetStringFromList(lstStrings):
    strFinal = ""
    if(lstStrings is not None and len(lstStrings)>0):
        for str in lstStrings:
            strFinal += str + ","
        strFinal.removesuffix(",")
    return strFinal


def ConvertFloatToNumString(num):