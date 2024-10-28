
class DBSettings:
    DBType = None
    Host = None
    Port = None
    DBName = None
    User = None
    Schema = None
    Password = None
    
    def __init__(self, dbType, host, port, dbname, user, schema, password):    
        self.DBType = dbType
        self.Host = host
        self.Port = port
        self.DBName = dbname
        self.User = user
        self.Schema = schema
        self.Password = password