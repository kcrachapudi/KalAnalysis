from sqlalchemy import create_engine
import Extractor, Loader
from CommonVMs import PortSnapVM
import Utils
import time
from pathlib import Path, PureWindowsPath
from Configurator import ConfigReader, ConfigDecoder, DictToObj
from DAL import DBSettings, DBConnector, DBLayer

configReader = None
FileLocation = None
SourceDBLayer = None

def Start():
    print("ETL Orchestrator Start")
    configReader = ConfigReader()

    Operation = configReader.GetAttribute("Operation")

    if(Operation == 'SourceDBtoTargetDB'):
        SourceDBConfig = GetConfigObject(configReader.GetAttribute("SourceDB"))
        SourceDBEngine:DBLayer.DBEngine = GetDBEngine(SourceDBConfig)
        TargetDBConfig = GetConfigObject(configReader.GetAttribute("TargetDB"))
        TargetDBEngine:DBLayer.DBEngine = GetDBEngine(TargetDBConfig)

        dfSourceTable = Extractor.ExtractTable(SourceDBEngine, SourceDBConfig.TableName)
        dfTargetTable = Extractor.ExtractTable(TargetDBEngine, TargetDBConfig.TableName)

        Loader.LoadTableData(TargetDBEngine, dfSourceTable, TargetDBConfig.TableName, deleteExisting=False)
    elif(Operation == 'SourceCSVtoTargetDB'):
        SourceCSVConfig = GetConfigObject(configReader.GetAttribute("SourceCSVConfig"))
        dfSourceTable = Extractor.ExtractCSV(SourceCSVConfig.FileLocation, SourceCSVConfig.FileName, SourceCSVConfig.CSVDelimiter)
        TargetDBConfig = GetConfigObject(configReader.GetAttribute("TargetDB"))
        TargetDBEngine:DBLayer.DBEngine = GetDBEngine(TargetDBConfig)

        Loader.LoadTableData(TargetDBEngine, dfSourceTable, TargetDBConfig.TableName, deleteExisting=True)
    elif(Operation == "MultiTableDataTransfer"):
        config = configReader.GetAttribute("MultiTableDataConfig")
        MultiTableDataConfig = GetConfigObject(config)
        SourceDBConfig = GetConfigObject(configReader.GetAttribute("SourceDB"))
        SourceDBEngine:DBLayer.DBEngine = GetDBEngine(SourceDBConfig)
        TargetDBConfig = GetConfigObject(configReader.GetAttribute("TargetDB"))
        TargetDBEngine:DBLayer.DBEngine = GetDBEngine(TargetDBConfig)
        for table in MultiTableDataConfig.Tables:
            dfSourceTable = Extractor.ExtractTable(SourceDBEngine, table)
            Loader.LoadTableData(TargetDBEngine, dfSourceTable, table, MultiTableDataConfig.DeleteExistingData)
    elif(Operation == 'MultiSourceCSVtoTargetDB'):
        MultSourceCSVConfig = GetConfigObject(configReader.GetAttribute("MultSourceCSVConfig"))
        dictData = Extractor.ExtractMultiCSV(MultSourceCSVConfig.FileLocation, MultSourceCSVConfig.CSVDelimiter) 
        dictTableNames = dict()
        for dkey in dictData:
            dictTableNames[dkey] = ''.join(dkey.split("_")[1].split(".")[0])
        TargetDBConfig = GetConfigObject(configReader.GetAttribute("TargetDB"))
        TargetDBEngine:DBLayer.DBEngine = GetDBEngine(TargetDBConfig)
        Loader.LoadMultiTableData(TargetDBEngine, dictData, dictTableNames, MultSourceCSVConfig.DeleteExistingData)

    print("ETL Orchestrator End")


def GetConfigObject(dbConfig):
    configObj = DictToObj(dbConfig)
    return configObj


def GetDBEngine(dbConfig):
    dbSettings:DBSettings.DBSettings = DBSettings.DBSettings(dbType=dbConfig.DBType, host = dbConfig.Host, port = dbConfig.Port, dbname = dbConfig.DBName, user = dbConfig.User, schema = dbConfig.Schema, password = dbConfig.Password)
    dbConnector = DBConnector.DBConnector(dbSettings)    
    dbEngine:DBLayer.DBEngine = DBLayer.DBEngine(dbCon=dbConnector.DBCon, dbVals=dbSettings)
    return dbEngine


Start()