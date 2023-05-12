import pandas as pd

class Company:
    Symbol: str = ''
    dfCompany: pd.DataFrame
    
    def __init__(self, symbol, dfTicker):
      self.Symbol = symbol
      self.dfCompany = dfTicker