import gspread
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy.orm import util
from ViewModels.CommonVMs import Holding, PortSnapVM

import DAL
from Utils import *
import datetime

transactions = []


def Connect(fileName, sheetName = None):
    print("Connecting to File " + fileName)
    # use creds to create a client to interact with the Google Drive API
    #scope = ['https://spreadsheets.google.com/feeds']
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credential = ServiceAccountCredentials.from_json_keyfile_name("GSheets.json", scope)
    client = gspread.authorize(credential)
    sheets = client.open(fileName).worksheets()
    currentsheet = None
    if(sheetName is not None):
        for cursheet in sheets:
            if(sheetName == cursheet.title):
                print('This is Selected Sheet')
                currentsheet = cursheet
                break
            else:
                continue
    return currentsheet


def ETLSingleGoogleSpreadsheet(fileName, sheetName):
    print(f'Loading GSheet {fileName} for Brokerage {sheetName}')
    psvm: PortSnapVM
    try:
        psvm = None
        psvm = LoadPortSnap(fileName, sheetName)
        #if(psvm is not None):
        #    Repo.SavePortSnapData(psvm)
        print(f'Completed ETLSingleGoogleSpreadsheet for File {fileName} for Brokerage {sheetName}')
    except:
        print(f'Exception in ETLSingleGoogleSpreadsheet for File {fileName} for Brokerage {sheetName}')


def ETLSingleCSVSheet(sheetName, brokerageName):
    csvPath = Path('C:/Users/Augustus/Desktop/BrokerageAccountSummary').resolve()
    print(f'Loading CSV {sheetName} for Brokerage {brokerageName}')
    psvm: PortSnapVM
    fileName = f'{sheetName} - {brokerageName}.csv'
    csvName = csvPath / fileName
    try:
        psvm = None
        psvm = CSVSheet.ExtractTransformSheet(csvName, brokerageName)
        if(psvm is not None):
            Repo.SavePortSnapData(psvm)
        print(f'Completed ETLSingleCSVSheet for File {csvName} for Brokerage {brokerageName}')
    except:
        print(f'Exception in ETLSingleCSVSheet for File {csvName} for Brokerage {brokerageName}')



def LoadPortSnap(fileName, sheetName=None):
    psvm = None
    gsheet = None
    try:
        print(f'******************************************    CONNECT to GSheet for {sheetName} ************************************')
        gsheet = Connect(fileName, sheetName)
        print(f'******************************************    SUCCESS in Connecting to GSheet for {sheetName} ************************************')
        if(gsheet is not None):
            try:
                print(f'******************************************    LOAD GSheet for {sheetName} ************************************')
                psvm = GetPortSnapData(gsheet)
                print(f'******************************************    SUCCESS in Loading GSheet for {sheetName} ************************************')
            except Exception as e:
                print(f'******************************************    EXCEPTION in GSheets.py->LoadPortSnap->InnerTry-> {sheetName} is {e} ************************************')
                raise
    except Exception as ex:
        print(f'******************************************    EXCEPTION in GSheets.py->LoadPortSnap->OuterTry-> {sheetName} exception is {ex} ************************************')
    return psvm


def GetPortSnapData(gsheet):
    psvm = None 
    holdings = None
    holdings = []
    if(gsheet is not None):
        try:
            #Access the row 1 and column 2
            #sheet1.cell(1, 2).value
            # or using A1 notation
            name = gsheet.acell('A2').value
            strsnapshotDate = gsheet.acell('B2').value
            snapshotDate = datetime.datetime.strptime(strsnapshotDate, "%m/%d/%Y").date()
            cash = DefaultFloat(gsheet.acell('F2').value)
            marginDebt = DefaultFloat(gsheet.acell('G2').value)  
            holdingrow = 5
            while IsHoldingRowValid(gsheet.cell(holdingrow, 1)):
                try:
                    symbol = gsheet.cell(holdingrow, 1).value
                    quantity = int(float(gsheet.cell(holdingrow, 2).value)) #int has a bug as it cannot convert floating point string, so convert to float first then to int
                    strbuyDate = gsheet.cell(holdingrow, 3).value
                    buyDate = datetime.datetime.strptime(strbuyDate, "%m/%d/%Y").date()
                    buyPrice = float(gsheet.cell(holdingrow, 4).value)
                    snapshotPrice = float(gsheet.cell(holdingrow, 7).value)
                    holding = Holding(symbol, quantity, buyDate, buyPrice, snapshotDate, snapshotPrice)
                    holdings.append(holding)
                    holdingrow += 1
                except Exception as e:
                    print(f'******************************************    EXCEPTION in GSheets.py->GetPortSnapData -> IsHoldingRowValid is -> {e} ************************************')
            psvm = PortSnapVM(name=name, snapshotDate=snapshotDate, cash=cash, marginDebt=marginDebt, holdings=holdings)
        except Exception as ex:
            print(f'******************************************    EXCEPTION in GSheets.py->GetPortSnapData -> OuterTry is -> {ex} ************************************')
    return psvm

def IsHoldingRowValid(cell):
    result = False
    if(cell is None or cell.value is None):
        result = False
    else:
        if(len(cell.value)>0):
            result = True
    return result

def GetSheetRecords(gsheet):
    # Find a workbook by name and open the first sheet
    #gsheet = client.open(sheetName).sheet1
    # Extract and print all of the values
    sheetRecords = gsheet.get_all_records()
    #print(sheetRecords)
    return sheetRecords


def ConvertRecordsToTransactions(sheetRecords):
    rows = 0
    brName = ''
    for record in sheetRecords:
        brName = ''
        trans = Transaction()
        brName = GetBrokerageName(SetValueOrNone(record['Account']))
        trans.BrokerageAccountID = DAL.GetBrokerageAccountIDByName(brName)
        trans.CompanyID = DAL.GetOrAddCompanyBySymbol(record['Company'])
        trans.Quantity = record['Quantity']
        trans.BuyDate = SetValueOrNone(record['BuyDate'])
        trans.BuyPrice = SetValueOrNone(record['SCP'])
        trans.SellDate = SetValueOrNone(record['SellDate'])
        trans.SellPrice = SetValueOrNone(record['SSP'])
        DAL.SaveDBObject(trans)
        rows = rows + 1
    print(str(rows) + ' Transactions Saved')
        

def GetBrokerageName(brName):
    defaultBrokerageName = 'BAML-28Z-42L08'
    if(brName is None):
        brName = defaultBrokerageName
    elif(brName == '28Z'):
        brName = defaultBrokerageName
    elif(brName == '22X'):
        brName = "BAML-22X-50219"
    return brName