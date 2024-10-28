import psycopg2
from sqlalchemy import create_engine, inspect, text as sql_text
from sqlalchemy import extract, distinct, asc, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd


class DBEngine:
    DBCon = None
    DBVals = None
    DBSession = None
    Base = None
    
    def __init__(self, dbCon, dbVals):
        self.DBCon = dbCon
        self.DBVals = dbVals
        self.DBSession = scoped_session(sessionmaker(bind=self.DBCon))
        # perform database reflection to analyze tables and relationships
        self.Base = automap_base()
        self.Base.prepare(self.DBCon, reflect=True)
        
    
    def GetTableNames(self):
        inspector = inspect(self.DBCon)
        return inspector.get_table_names()


    def GetTableData(self, tableName:str)->pd.DataFrame:
        decoratedTableName = self.DecorateTableName(tableName)
        sql = f'SELECT * FROM {decoratedTableName}'
        df = pd.read_sql(sql, con=self.DBCon)
        #query=sql_text(sql)        
        #df = pd.read_sql(query, con=self.DBCon)
        return df

    def GetQueryData(self, query):
        return pd.read_sql(query, con=self.DBCon)
    
    
    def DecorateTableName(self, tableName):
        return f'{self.DBVals.Schema}."{tableName}"'


    def DeleteAllFromTable(self, tableName):
        return f''


    def TruncateTable(self, tableName):
        query = f'TRUNCATE TABLE {tableName}'
        sqlquery = sql_text(query)
        self.DBSession.execute(sqlquery)
        self.DBSession.commit()


    def GetDBUUID(self):
        sql = f'select * from uuid_generate_v4()'
        dfUUID = pd.read_sql(sql, con=self.DBCon)
        uuid = dfUUID.iloc[0,0]
        return uuid

    
    def CreateWatchlist(self, watchlistname:str, watchlistdescription:str):
        decoratedTableName = self.DecorateTableName('watchlist')        
        Tab = self.Base.classes.watchlist
        result = 0
        watchlistid = self.GetDBUUID()
        instance = Tab(id=watchlistid, name=watchlistname, description=watchlistdescription)
        self.DBSession.add(instance)
        self.DBSession.commit()


    def GetWatchlistNames(self)->pd.DataFrame:
        decoratedTableName = self.DecorateTableName('watchlist')
        sql = f'SELECT * FROM {decoratedTableName}'
        dfData = pd.read_sql(sql, con=self.DBCon)
        return dfData["name"]


    def GetWatchlistSymbols(self, watchlistname:str):
        decoratedTableName = self.DecorateTableName('watchlistsymbols')
        sql = f"select id as udfier, symbol from watchlistsymbols where watchlistname = '{watchlistname}'"
        dfData = pd.read_sql(sql, con=self.DBCon)
        return dfData


    def GetCompanies(self):
        decoratedTableName = self.DecorateTableName('company')
        sql = f"select * from {decoratedTableName} order by here watchlistname = '{watchlist}'"
        dfData = pd.read_sql(sql, con=self.DBCon)
        return edfWatchlistDetails


    def SaveWatchlistData(self, datData, watchlist:str):
        decoratedTableName = self.DecorateTableName('watchlistsymbols')        
        TabWatchlistSymbols = self.Base.classes.watchlistsymbols
        result = 0
        if(datData is None):
            pass
        else:
            addedrows = datData["added_rows"]
            addinstances=[]
            for addedrow in addedrows:
                watchlistid = self.GetDBUUID()
                addinstances.append(TabWatchlistSymbols(id=watchlistid, symbol=addedrow['symbol'], watchlistname=watchlist))
            self.DBSession.add_all(addinstances)
            self.DBSession.commit()


