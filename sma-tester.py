import pandas as pd
from pathlib import Path
from Utils import Utils
from AIML.AIML_sma import SMAML

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

# Unit Test the sma.py and sma_ml.py 
ticker = 'NVDA'
dfSymbol = Utils.GetLocalTickerData(ticker)
capital = float(10000)

shortwindow1 = 50
longwindow1 = 200

# Test the Basic algo for the 50-200 SMA Windows
#smaA = SMA('NVDA', dfSymbol, capital, shortwindow1, longwindow1)
# Test the SVM ML algo for the 50-200 SMA Windows
smamlA1 = SMAML('NVDA', dfSymbol, capital, shortwindow1, longwindow1, 'svm')    
# Test the LR ML algo for the 50-200 SMA Windows
smamlA2 = SMAML('NVDA', dfSymbol, capital, shortwindow1, longwindow1, 'lr')    
# Test the DTC ML algo for the 50-200 SMA Windows
smamlA3 = SMAML('NVDA', dfSymbol, capital, shortwindow1, longwindow1, 'dtc')    

shortwindow2 = 10
longwindow2 = 50

# Test the Basic algo for the 10-50 SMA Windows
#smaB = SMA('NVDA', dfSymbol, capital, shortwindow2, longwindow2)
# Test the SVM ML algo for the 10-50 SMA Windows
smamlB1 = SMAML('NVDA', dfSymbol, capital, shortwindow2, longwindow2, 'svm')    
# Test the LR ML algo for the 10-50 SMA Windows
smamlB2 = SMAML('NVDA', dfSymbol, capital, shortwindow2, longwindow2, 'lr')    
# Test the DTC ML algo for the 10-50 SMA Windows
smamlB3 = SMAML('NVDA', dfSymbol, capital, shortwindow2, longwindow2, 'dtc')    
