# Imports
import os
import numpy as np
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from regex import P
import yfinance as yf

import hvplot.pandas
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier 

class SMAML:
    #Class variables needed for ML Analysis
    ticker = ''
    capital = 0
    short_window = 0
    long_window = 0

    total_trades = 0
    gain_trades = 0
    loss_trades = 0 
    max_profit_trade = 0
    max_loss_trade = 0
    totalTradeProfitLoss = 0
    total_portfolio_value = 0 
    finalProfitLoss = 0

    svm_model = None
    X_train_scaled = None
    X_test_scaled = None
    y_train = None
    y_test = None
    dfMain = None
    dfFinal = None
    mlModelName = None

    def __init__(self, symbol, dfSymbol, initcapital, swindow, lwindow, mlClassifier):
        # This method is the main entry point for this class
        # All the logic in this class flows from this method
        #Initialize the variables from the input variables provided in the parameters list

        self.ticker = symbol
        self.capital = initcapital
        self.short_window = swindow
        self.long_window  = lwindow

        print(f'*********************************************************************************************************************************')

        # Call the Machine Learning SMA Analysis method and pass in the Ticker dataframe and the ML Model type
        # The SMA Analysis returns back a dataframe dfSignal
        dfSignal = self.SMAMLAnalysis(dfSymbol, mlClassifier)

        self.Summary()
        print(f'---------------------------------------------------------------------------------------------------------------------------------')
 


    def SMAMLAnalysis(self, dfTrading, mlClassifier):
        # Calculate the daily returns using the closing prices and the pct_change function
        dfTrading["actual_returns"] = dfTrading["Close"].pct_change()

        # Drop all NaN values from the DataFrame
        dfTrading = dfTrading.dropna()
    
        # Create a simple moving average (SMA) using the short_window and assign this to a new columns called sma_fast
        dfTrading['sma_fast'] = dfTrading['Close'].rolling(window=self.short_window).mean()
        
        # Create a simple moving average (SMA) using the long_window and assign this to a new columns called sma_slow
        dfTrading['sma_slow'] = dfTrading['Close'].rolling(window=self.long_window).mean()

        # Drop the NaNs using dropna()
        dfTrading = dfTrading.dropna()

        # Assign a copy of the sma_fast and sma_slow columns to a new DataFrame called X
        X = dfTrading[['sma_fast', 'sma_slow']].copy()

        # Create a new column in the dfTrading called signal setting its value to zero.
        dfTrading['signal'] = 0.0

        # Create the signal to buy
        dfTrading.loc[(dfTrading['actual_returns'] >= 0), 'signal'] = 1

        # Create the signal to sell
        dfTrading.loc[(dfTrading['actual_returns'] < 0), 'signal'] = -1

        # Copy the new signal column to a new Series called y.
        y = dfTrading['signal'].copy()

        # Select the start of the training period
        training_begin = X.index.min()

        # Select the ending period for the training data with an offset of 3 months
        training_end = X.index.min() + DateOffset(months=3)

        # Generate the X_train and y_train DataFrames
        X_train = X.loc[training_begin:training_end]
        self.y_train = y.loc[training_begin:training_end]

        # Generate the X_test and y_test DataFrames
        self.X_test = X.loc[training_end:]
        self.y_test = y.loc[training_end:]

        # Create a StandardScaler instance
        scaler = StandardScaler()
        
        # Apply the scaler model to fit the X-train data
        X_scaler = scaler.fit(X_train)
        
        # Transform the X_train and X_test DataFrames using the X_scaler
        self.X_train_scaled = X_scaler.transform(X_train)
        self.X_test_scaled = X_scaler.transform(self.X_test)

        #Save it to main object for reuse later
        self.dfMain = dfTrading

        #Make a decision here as to what ML Model to use
        #We get the mlCLassifier input to select the ML Model
        if(mlClassifier == 'svm'):
            self.SVM()
            self.mlModelName = 'Support Vector Machine (SVM)'
        elif(mlClassifier =='lr'):
            self.LR()
            self.mlModelName = 'Logistic Regression (LR)'
        elif(mlClassifier =='dtc'):
            self.DTC()
            self.mlModelName = 'Decision Tree Classifier (DTC)'



    def SVM(self):
        # Create the SVM classifier model
        self.svm_model = svm.SVC()
        
        # Fit the model to the data using X_train_scaled and y_train
        self.svm_model = self.svm_model.fit(self.X_train_scaled, self.y_train)

        # Use the trained model to predict the trading signals for the training data
        training_signal_predictions = self.svm_model.predict(self.X_train_scaled)

        # Display the sample predictions
        training_signal_predictions[:10]
    
        # Evaluate the model using a classification report
        training_report = classification_report(self.y_train, training_signal_predictions)
        #print(training_report)
    
        dfTrading = self.dfMain
    
        # Use the trained model to predict the trading signals for the testing data.
        testing_signal_predictions = self.svm_model.predict(self.X_test_scaled)
        # Evaluate the model's ability to predict the trading signal for the testing data
        svm_testing_report = classification_report(self.y_test, testing_signal_predictions)
        #print(svm_testing_report)

        # Create a new empty predictions DataFrame using code provided below.
        predictions_df = pd.DataFrame(index=self.X_test.index)
        predictions_df["predicted_signal"] = testing_signal_predictions
        predictions_df["actual_returns"] = dfTrading["actual_returns"]
        predictions_df["trading_algorithm_returns"] = predictions_df["actual_returns"] * predictions_df["predicted_signal"]
        predictions_df.head()

        # Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns`
        dfFinal = (1 + predictions_df[["actual_returns", "trading_algorithm_returns"]]).cumprod()
        
        #Use this for later analysis and backtesting
        self.dfFinal = dfFinal


    def LR(self):
        # Create an instance of the LogisticRegression model
        logistic_regression_model = LogisticRegression()
        
        # Fit the LogisticRegression model
        logistic_regression_model.fit(self.X_train_scaled, self.y_train)
        
        # Use the trained LogisticRegression model to predict the trading signals for the training data
        lr_training_signal_predictions = logistic_regression_model.predict(self.X_train_scaled)
        
        # Generate a classification report using the training data and the logistic regression model's predications
        lr_training_report = classification_report(self.y_train, lr_training_signal_predictions)
        # Review the classification report
        #print(lr_training_report)

        dfTrading = self.dfMain

        # Use the trained model to predict the trading signals for the testing data.
        lr_testing_signal_predictions = logistic_regression_model.predict(self.X_test_scaled)
        # Generate a classification report using the testing data and the logistic regression model's predications
        lr_testing_report = classification_report(self.y_test, lr_testing_signal_predictions)

        # Review the classification report
        #print(lr_testing_report)

        # Create a new empty predictions DataFrame using code provided below.
        predictions_df = pd.DataFrame(index=self.X_test.index)
        predictions_df["predicted_signal"] = lr_testing_signal_predictions
        predictions_df["actual_returns"] = dfTrading["actual_returns"]
        predictions_df["trading_algorithm_returns"] = predictions_df["actual_returns"] * predictions_df["predicted_signal"]
        predictions_df.head()

        # Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns`
        dfFinal = (1 + predictions_df[["actual_returns", "trading_algorithm_returns"]]).cumprod()
        
        #Use this for later analysis and backtesting
        self.dfFinal = dfFinal



    def DTC(self):
        # Create the Decition Tree classifier model
        dtc_model = DecisionTreeClassifier()
        
        # Fit the model to the data using X_train_scaled and y_train
        dtc_model = dtc_model.fit(self.X_train_scaled, self.y_train)

        # Use the trained model to predict the trading signals for the training data
        training_signal_predictions = dtc_model.predict(self.X_train_scaled)

        # Display the sample predictions
        training_signal_predictions[:10]
    
        # Evaluate the model using a classification report
        training_report = classification_report(self.y_train, training_signal_predictions)
        #print(training_report)
    
        dfTrading = self.dfMain
    
        # Use the trained model to predict the trading signals for the testing data.
        testing_signal_predictions = dtc_model.predict(self.X_test_scaled)
        # Evaluate the model's ability to predict the trading signal for the testing data
        dtc_testing_report = classification_report(self.y_test, testing_signal_predictions)
        #print(dtc_testing_report)

        # Create a new empty predictions DataFrame using code provided below.
        predictions_df = pd.DataFrame(index=self.X_test.index)
        predictions_df["predicted_signal"] = testing_signal_predictions
        predictions_df["actual_returns"] = dfTrading["actual_returns"]
        predictions_df["trading_algorithm_returns"] = predictions_df["actual_returns"] * predictions_df["predicted_signal"]
        predictions_df.head()

        # Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns`
        dfFinal = (1 + predictions_df[["actual_returns", "trading_algorithm_returns"]]).cumprod()
        
        #Use this for later analysis and backtesting
        self.dfFinal = dfFinal



    def Summary(self):
        # Use the analyzed and backtested data to summarize the results
        print(f'Analysis Summary for {self.ticker}')
        ending_value = self.dfFinal.iat[-1, 1] 
        appreciation_pct = round(ending_value * 100, 2)
        final_investment = self.capital * ending_value
        finalProfitLoss = final_investment - self.capital
        print(f'Analysis Type: Simple Moving Average Crossover({self.short_window}, {self.long_window}) with Machine Learning {self.mlModelName}') 
        print(f'Initial Capital: ${round(self.capital,2)}')
        print(f'Total Trade/Profit Loss: ${round(finalProfitLoss,2)} ')
        print(f'Final Investment Value : ${round(final_investment, 2)}')
        
