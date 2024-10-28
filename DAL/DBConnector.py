import psycopg2
from sqlalchemy import create_engine, inspect
from DAL import DBSettings

class DBConnector:
    dbSettings: DBSettings.DBSettings = None
    DBCon = None
    
    def __init__(self, dbSettings):    
        self.dbSettings = dbSettings
        self.CreateEngine()


    def CreateEngine(self):
        try:
            if(self.dbSettings.DBType == 'postgres'):
                self.DBCon = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.dbSettings.User, self.dbSettings.Password, self.dbSettings.Host,self.dbSettings.Port,self.dbSettings.DBName))
        except Exception as ex:
            print("Error while connecting to Database", ex)        
