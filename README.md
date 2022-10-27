# FinAdvisorsAI

### Project Overview

At FinAdvisorsAI, we strive to put the power of AI into the hands of everyday investors.  In our latest update, we have created 2 Simple Moving Average algorithims that can be utilized with personalized stock selections.  Our algorithims are back tested with each investors risk, return, and stock profile that they input into our program. A lot of times in investing, investors want to know how they can make better investment choices by reducing "uncertainty and risk" and that's where FinAdvisorsAI steps in.  We utilize 3 machine learning models to help investors navigate through potential risk/return prfoile scenarios and outcomes.  Our machine learning models are compared to both of our base line algorithims and displayed next to each other for a quick analysis of profit/loss. In the end, our goal of placing the power of AI in the hands of everyday investors should help provide better risk management for investors present and future selves.  

**Past returns are for illustrative purposes only and do not guarantee future returns.  We do not guarantee any returns or outcomes.  Investing involves risks including and not limited to complete loss of principal.**


### Technologies/Installation Guide

- ```from datetime import datetime```

- ```import pandas as pd```

- ```from pathlib import Path```

- ```import numpy as np```

- ```import questionary```

- ```import cloud_data_collector```

- ```from customer import Customer```

- ```import Utils```

- ```import datetime```

- ```import matplotlib```

- ```import matplotlib_inline```

- ```from sma import SMA```

- ```from sma_ml import SMAML```

- ```import imp```

- ```import os```

- ```from dotenv import load_dotenv```

- ```from regex import P```

- ```import yfinance as yf```

- ```import hvplot.pandas```

- ```from pandas.tseries.offsets import DateOffset```

- ```from sklearn.preprocessing import StandardScaler```

- ```from sklearn import svm```

- ```from sklearn.metrics import classification_report```

- ```from sklearn.linear_model import LogisticRegression```

- ```from sklearn.tree import DecisionTreeClassifier```

# Usage

## The program will ask an investor a series of questions to help screen out 3 stocks in which they will choose 1 of them to run in our algorithms and machine learning models.  The questions we ask them are what is their risk tolerance, expected minimum return, and the amount they would like to invest.  Once they answer those 3 questions, they will be presented with 3 stock options.  They choose one of the options and then let FinAdvisorsAI program take over from there.  

## Step 1: Get Ticker Data from YFinance for Selected Tickers. Selected Tickers could be from any source that the customer wants. It could be from a Excel spreadsheet, from an email or just from a conversation with the customer that can be input into a list of Tickers. These Tickers are then sent to YFinance API to collect 5 years worth of stock data. The 5 years we selected is just for a starter but we can input 10 years or 20 years if need be and the program will handle it pulling the data from YFinance. Once the ticker data is available then the Program does some important calculations to find the Annualized returns, Standard deviations, Sharpe ratios etc and shows it to the customer in detail so that the Customer can make an informed decision on how to proceed further. The first input that the program seeks from the Customer is the Risk appetite they have for Investing. So the program sorts the stocks on the Risk profile and asks them to choose a Risk profile they are comfortable with. The profile that they choose will help filter out the stocks that have a higher risk than what they chose. Below is a screenshot of how this looks.

![ss_1](screenshot1_proj2.png)


## Step 2: Once the Customer chooses a Risk Profile then the stocks that have higher risk are filtered out. The remaining stocks are shown sorted by their returns. The programs asks for the Customer to choose a Return percent as a number. Once the Customer chooses a number say 8, then the program filters out the stocks that do not meet that return and shows only those stocks that meet the chosen return or exceed it. The program ensures that the return selected is not too high as it may filter out all stocks resulting in nothing to continue further analysis on. Hence it makes sure atleast 3 stocks remain after filtering out the rest. 
![ss_2](screenshot2_proj2.png)

## Step 3: The program then selects the top 3 best performing stocks for further analysis. The next thing the program requests the customer is to input their Investment Amount. 
![ss_3](screenshot3_proj2.png)

## Step 4: Once the Investment Amount is input the program requests the customer to input one out of the three best performing stocks. This Stock will be then used for the Trading Algorithm followed by Machine Learning analysis. 
![ss_4](screenshot4_proj2.png)

## Step 5: Once a stock is selected say (MSFT) in our example then the program starts looking at the SMA Moving Crossover Trading Algorithm Analysis followed by Machine Learning Models Analysis. We are focused on Simple Moving Average Crossover Algorithms and for this exercise we are focused on 2 different timeframes for the long and short window moving averages. First is the 50 and 200 SMA crossover Analysis. The Program analyses this for a long strategy to buy when the 50 SMA crosses the 200 SMA to the upside. Similarly the Algo tries to sell when the 50 SMA crosses the 200 SMA to the downside. Once the Algo is done with it we back test the Algo with the stock closing data that is available to see how the Algo performed. Then we continue the Analysis forward with 3 Machine Learning Models, a). SVM Model (Support Vector Machine), b). LR Linear Regression Classification Model, c).DTC Model DecisionTreeClassifier. 
![ss_5](screenshotA1.png)

## Step 6: We proceed with the next phase of the Analysis with a SMA timeframe of 10-50. We buy when the 10 SMA crosses the 50 SMA to the upside and sells when the 10 SMA crosses the 50 SMA to the downside. Once the Algo is done with it we back test the Algo with the stock closing data that is available to see how the Algo performed. Then we continue the Analysis forward with 3 Machine Learning Models, a). SVM Model (Support Vector Machine), b). LR Linear Regression Classification Model, c).DTC Model DecisionTreeClassifier. 
![ss_6](screenshotA2.png)

## Setp 7: In total we get 8 Outcomes, 
## First 50-200 Baseline, 50-200 SVM, 50-200 LR, 50-200 DTC
## Second 10-50 Baseline, 10-50 SVM, 10-50 LR, 10-50 DTC.

<BR><BR><BR>
# Conclusion: After having run the 2 Baselines and 6 ML models for the 2 timeframes (50, 200) and (10, 50) we find that the SVM ML Model outperforms the other two ML Models as well as the Baselines consistently to a degree of 80% of the time. 
<BR><BR><BR>

**A side note: We have included a BONUS algorithim focused on the Relative Strength Index that is not part of any analysis as of now but that we would like to include in the future.  It is a momentum indicator that follows a stock price pattern/movment and indicates when a stock is overbought and oversold. The Algo purpose is to buy at prices when the indicator's RSI is oversold and to then sell when the indicator RSI has reached overbought. Find this Algo in RSI_algo.ipynb**

---
<BR><BR><BR>

## Contributors

- Kalyan Rachapudi

- James Willis

- Severo Fernandez

- Allyssa Carmin

- Daniel Boyne




