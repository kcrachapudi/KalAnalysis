import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy.orm import util
from CommonVMs import Holding, PortSnapVM
from Utils import *
import datetime
import psycopg2
from sqlalchemy import create_engine, inspect, extract, distinct, asc, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
from DAL import DBLayer, DBSettings, DBConnector
import os

transactions = []


def ExtractTable(dbEngine, tableName):
    dfData = dbEngine.GetTableData(tableName)
    return dfData


def ExtractCSV(fileLocation, fileName, csvDelimiter):
    curfile = os.path.join(fileLocation, fileName)
    dfData = pd.read_csv(curfile, sep=csvDelimiter)
    return dfData


def ExtractMultiCSV(fileLocation, csvDelimiter):
    dictData = dict()
    files = []
    for x in os.listdir(fileLocation):
        if x.endswith(".csv"):
            # Prints only text file present in My Folder
            files.append(x)
    files.sort()
    dfTab:pd.DataFrame
    for file in files:
        dfTab = ExtractCSV(fileLocation, file, csvDelimiter)
        dictData[file] = dfTab
    return dictData