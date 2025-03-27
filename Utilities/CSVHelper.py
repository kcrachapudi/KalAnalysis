import csv
from io import StringIO  
import pandas as pd
from pathlib import Path

def ETLCSVtoDataFrame(file, filedatatype):
    records = []
    dfData = pd.DataFrame()
    if(filedatatype =='string'):
        # To convert to a string based IO:
        file = StringIO(file.getvalue().decode("utf-8"))
        # To read file as string:
        file_data = file.read()

        for line in open(file_data):
            line = line.strip()  # strip '\n'
            if line==',':
                continue           # ignore empty line
            records.append(line.rstrip(','))
    elif(filedatatype=='bytes'):
        sline:str
        for line in file.readlines():
            sline = line.decode() # convert from byte string to string
            sline = sline.strip()  # strip '\n'
            if sline==',':
                continue           # ignore empty line
            records.append(sline.rstrip(','))

        # Combine the strings into a single CSV string
        line_data = "\n".join(records)

        # Create a StringIO object from the CSV string
        iodata = StringIO(line_data)

        # Read the CSV data into a DataFrame
        dfData = pd.read_csv(iodata)   
    return dfData


def GetCSVDataFromResources(fileName, indexCol) -> pd.DataFrame:
    dfData:pd.DataFrame = pd.DataFrame()
    try:
        absdir = Path(__file__).parent.absolute()
        csvreadpath = Path(f'{absdir}/../Resources/{fileName}')
        dfData = pd.read_csv(Path(csvreadpath), index_col=indexCol, parse_dates=True, infer_datetime_format=True)
    except Exception as ex:
        print(f'Error in getting csv data for {fileName} . Error is {ex}')      
    return dfData


def GetLocalCSVData(fileName:str, location:str)->pd.DataFrame:
    dfData:pd.DataFrame
    try:
        csvpath = Path(f'{location}/{fileName}')
        dfData = pd.read_csv(Path(csvpath))
    except Exception as ex:
        print(f'Error in getting data {ex}')      
    return dfData

