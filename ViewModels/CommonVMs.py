from email import utils
from sqlalchemy.sql.expression import false
from datetime import *

from Utils import *

class DebugVM:
    ConfigString = ''
    SQLDBString = ''
    

class TransactionSnapshotSummary:
    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    jun = 0
    jul = 0
    aug = 0
    sep = 0
    oct = 0
    nov = 0
    dec = 0

    def yeartotal(self):
        return self.jan + self.feb + self.mar + self.apr + self.may + self.jun + self.jul + self.aug + self.sep + self.oct + self.nov + self.dec


class TransactionSnapshotShowHideComponents:
    showCard = False
    showTable = False
    showSummary = False


class PortfolioSummaryVM:
    BrokerageAccountID = ''
    TotalAccountValue = 0
    TotalCostBasis = 0
    TotalMarketValue = 0
    Cash = 0
    MarginDebt = 0
    TotalPLAmount = 0
    TotalPLPercent = 0
    def yeartotal(self):
        return self.jan + self.feb + self.mar + self.apr + self.may + self.jun + self.jul + self.aug + self.sep + self.oct + self.nov + self.dec


class BrokerageAccountSnapshotVM:
    ID = ''
    BrokerageAccountID = ''
    SnapshotDate = None
    TotalAccountValue = 0
    TotalCostBasis = 0
    TotalMarketValue = 0
    Cash = 0
    MarginDebt = 0
    TotalPLAmount = 0
    TotalPLPercent = 0
    def Init(self, basnapshot):
        basnapshot.Init()
        self.ID = basnapshot.ID
        self.BrokerageAccountID = basnapshot.BrokerageAccountID
        self.SnapshotDate = basnapshot.SnapshotDate
        self.Cash = basnapshot.CashValue
        self.MarginDebt = basnapshot.MarginUsed
        self.TotalCostBasis = basnapshot.TotalCostBasis
        self.TotalMarketValue = basnapshot.TotalMarketValue
        self.TotalPLAmount = basnapshot.TotalProfitLoss
        self.TotalPLPercent = basnapshot.TotalPLPercent
        self.TotalAccountValue = basnapshot.TotalAccountValue


class PortSnapVM:
    Name = None
    BrokerageAccountID = None
    SnapshotDate = None
    Cash = 0
    MarginDebt = 0
    TotalCostBasis = None
    TotalMarketValue = None
    TotalPLAmount = None
    TotalPLPercent = None
    TotalAccountValue = None
    MaxDaysOnMarket = None
    MarginDebtPercent = None
    __TotalVal = None
    Holdings = []

    def __CalcTotalCostBasis(self):
        if(self.TotalCostBasis is None):
            sum = 0
            for h in self.Holdings:
                try:
                    sum += DefaultAmount(h.BuyAmount)
                except:
                    pass    
            self.TotalCostBasis = sum
    def __CalcTotalMarketValue(self):
        if(self.TotalMarketValue is None):
            sum = 0
            for h in self.Holdings:
                try:
                    sum += DefaultAmount(h.MarketValue)
                except:
                    pass
            self.TotalMarketValue = sum
    def __CalcTotalPLAmount(self):
        self.TotalPLAmount =  DefaultAmount(self.TotalMarketValue) - DefaultAmount(self.TotalCostBasis)
    def __CalcTotalPLPercent(self):
        percent = 0
        try:
            percent = round((( DefaultAmount(self.TotalMarketValue) - DefaultAmount(self.TotalCostBasis))/ DefaultAmount(self.TotalCostBasis))*100)
        except:
            pass
        self.TotalPLPercent = percent
    def __CalcTotalAccountValue(self):
        self.__TotalVal = DefaultAmount(self.TotalMarketValue) + DefaultAmount(self.Cash)
        self.TotalAccountValue = self.__TotalVal - DefaultAmount(self.MarginDebt)
    def __CalcMaxDaysOnMarket(self):
        h:Holding
        self.MaxDaysOnMarket = max(h.DaysOnMarket for h in self.Holdings)
    def __CalcMarginDebtPercent(self):
        self.MarginDebtPercent = round((DefaultAmount(self.MarginDebt)/DefaultAmount(self.__TotalVal)) * 100)

    def __init__(self, name, snapshotDate, cash, marginDebt, holdings):
        self.Name = name
        self.SnapshotDate = snapshotDate
        self.Cash = cash
        self.MarginDebt = marginDebt
        self.Holdings = []
        if(holdings is not None and len(holdings)>0):
            if(isinstance(holdings[0], Holding)):
                for holding in holdings:
                    self.Holdings.append(holding)
            elif isinstance(holdings[0], MBAapp.models.BrokerageAccountSnapshotHolding):
                for holding in holdings:
                    VMHolding = Holding(holding.ParentCompany.Symbol, holding.Quantity, holding.BuyDate, holding.BuyPrice, holding.SnapshotDate, holding.SnapshotPrice, holding.ID)
                    self.Holdings.append(VMHolding)
            # Do other important Calculations based on Holdings and Account values
            self.__CalcTotalCostBasis()
            self.__CalcTotalMarketValue()
            self.__CalcTotalPLAmount()
            self.__CalcTotalPLPercent()
            self.__CalcTotalAccountValue()
            self.__CalcMarginDebtPercent()


class Holding:
    HoldingID = None
    Symbol = None
    Quantity = None
    BuyDate = None
    BuyPrice = None
    SnapshotDate = None
    SnapshotPrice = None
    BuyAmount = None
    MarketValue = None
    PLAmount = None
    PLPercent = None
    DaysOnMarket = None
    def __init__(self, symbol, quantity, buydate, buyprice, snapshotdate, snapshotprice, holdingID = None):
        self.Symbol = symbol
        self.Quantity = quantity
        self.BuyDate = buydate
        self.BuyPrice = buyprice
        self.SnapshotDate = snapshotdate
        self.SnapshotPrice = snapshotprice
        self.HoldingID = holdingID
        self.__CalcBuyAmount()
        self.__CalcMarketValue()
        self.__CalcPLAmount()
        self.__CalcPLPercent()
        self.__CalcDaysOnMarket()
    def __CalcBuyAmount(self):
        self.BuyAmount = self.Quantity * self.BuyPrice
    def __CalcMarketValue(self):
        self.MarketValue = self.Quantity * self.SnapshotPrice
    def __CalcPLAmount(self):
        self.PLAmount = self.MarketValue - self.BuyAmount
    def __CalcPLPercent(self):
        try:
            self.PLPercent = round(((self.MarketValue - self.BuyAmount)/self.BuyAmount)*100)
        except:
            self.PLPercent = 0
    def __CalcDaysOnMarket(self):
        try:
            timedelta = self.SnapshotDate - self.BuyDate
            self.DaysOnMarket = timedelta.days
        except:
            self.DaysOnMarket = 0


class TranceVM:
    BrokerageAccountName = ''
    CompanyName = ''
    tranche = ''


class BrokerageAccountNetWorthVM:
    Name = ''
    TotalAccountValue = 0
    TotalCostBasis = 0
    TotalMarketValue = 0
    Cash = 0
    MarginDebt = 0
    TotalPLAmount = 0
    TotalPLPercent = 0


class NetWorthVM:
    BrokerageAccountVMList=[]
    PortSnapVMList = []
    def __init__(self):
        self.BrokerageAccountVMList = None
        self.BrokerageAccountVMList = []
        self.PortSnapVMList = []
    @property
    def NetCostBasis(self):
        return self.__GetNetCostBasis()
    def __GetNetCostBasis(self):
        return self.__round(sum(bravm.TotalCostBasis for bravm in self.BrokerageAccountVMList))

    @property
    def NetMarketValue(self):
        return self.__GetNetMarketValue()
    def __GetNetMarketValue(self):
        return self.__round(sum(bravm.TotalMarketValue for bravm in self.BrokerageAccountVMList))               

    @property
    def NetCash(self):
        return self.__GetNetCash()
    def __GetNetCash(self):
        return self.__round(sum(bravm.Cash for bravm in self.BrokerageAccountVMList))                

    @property
    def NetMarginDebt(self):
        return self.__GetNetMarginDebt()
    def __GetNetMarginDebt(self):
        return self.__round(sum(bravm.MarginDebt for bravm in self.BrokerageAccountVMList))

    @property
    def NetPLAmount(self):
        return self.__GetNetPLAmount()
    def __GetNetPLAmount(self):
        return self.__round(self.NetMarketValue - self.NetCostBasis)

    @property
    def NetWorth(self):
        return self.__GetNetWorth()
    def __GetNetWorth(self):
        return self.__round(self.NetMarketValue + self.NetCash - self.NetMarginDebt)

    def __round(self,num):
        return 0 if num is None else round(num, 2)