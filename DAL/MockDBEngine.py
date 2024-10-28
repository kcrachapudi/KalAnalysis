import DBLayer
import pandas as pd
import DBSettings
import DBConnector2

def GetDBEngine():
    dbType = 'postgres'
    host = "localhost"
    port = 5432
    dbname = "MBA"
    user = "mbauser"
    password = "mbauser"
    schema = "public"
    dbType = 'postgres'

    dbSettings:DBSettings.DBSettings = DBSettings.DBSettings(dbType=dbType, host=host, port=port, dbname=dbname, user=user, schema=schema, password=password)
    dbConnector = DBConnector2.DBConnector2(dbSettings)    
    dbEngine = DBLayer.DBEngine(dbCon=dbConnector.DBCon, dbVals=dbSettings)
    return dbEngine