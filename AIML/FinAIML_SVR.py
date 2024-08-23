from os import close
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import BackTestFinal, BackTestInitial, Utils, DataPreparer, Helper, Numpyer
import holoviews as hv
import numpy as np
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import svm, linear_model
from sklearn.metrics import classification_report
from sklearn.model_selection import TimeSeriesSplit
from sklearn.compose import ColumnTransformer
from enum import StrEnum
import matplotlib. pyplot as plt


from math import ceil

from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib. dates as mandates
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn import preprocessing
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

import datetime


class FinAIML_SVR:
    
    def __init__(self, dfData, featureColumns, targetColName, predictionColName, train_data_percent, validation_data_percent, test_data_percent, initCapital):
        #Gather Parameters    
        self.dfData:pd.DataFrame = dfData
        self.FeatureCols = featureColumns
        self.TargetCol = targetColName
        self.PredictedCol = predictionColName

        self.trainDataPercent = train_data_percent
        self.validationDataPercent = validation_data_percent
        self.testDataPercent = test_data_percent
        self.initialCapital = initCapital

        #State
        self.X:pd.DataFrame
        self.y:pd.DataFrame
        self.training_begin = None
        self.training_end = None
        
        self.X_train = None
        self.y_train = None
        self.X_validation = None
        self.y_validation = None
        self.X_test = None
        self.y_test = None
        
        self.scaler = None
        self.X_scaler = None
        self.X_scaled = pd.DataFrame
        self.X_train_scaled = None
        self.X_test_scaled = None
        self.X_special_train = None
        self.X_special_test = None
        
        self.trainX = None
        self.testX = None
        
        self.model = None
        self.dfPredictions:pd.DataFrame
        self.TestingSignalPredictions = None
        self.TrainingClassificationReport = None
        self.TestingClassificationReport = None
        self.dfTrainingReport:pd.DataFrame
        self.dfTestingReport:pd.DataFrame
        
        self.cumprod1 = None
        self.cumprod2 = None
        self.cumprodplot1 = None
        self.cumprodplot2 = None
        self.dfFinal = None

        #Summary
        self.appreciation_pct = 0
        self.total_trades = 0
        self.gain_trades = 0
        self.loss_trades = 0 
        self.max_profit_trade = 0
        self.max_loss_trade = 0
        self.totalTradeProfitLoss = 0
        self.total_portfolio_value = 0 
        self.finalProfitLoss = 0


    def Orchestrate(self):
        #self.Main()
        self.Main2(self.dfData)
        init_close_null_count = self.dfData['Close'].isnull().sum()
        print('Initial Number of null values:', init_close_null_count)
        pass
       

    def Main2(self, dfMain:pd.DataFrame):
        dfOrig = dfMain.copy()
        dfOrig.drop(self.TargetCol, axis=1, inplace=True)
        # add outcome variable
        dfTarget = pd.DataFrame(data = dfMain[self.TargetCol])

        # finally, split into train-test
        X_train, X_test, y_train, y_test = train_test_split(dfOrig, dfTarget, train_size = self.trainDataPercent)

        model = self.CreateModel('SVR')
        model.fit(X_train, y_train.values.ravel())

        y_pred = model.predict(X_test)
        y_test[self.PredictedCol] = y_pred

        dfFinal = pd.merge(dfOrig, y_test, how = 'left', left_index = True, right_index = True)
        print(dfFinal.head())
        print(dfFinal.tail())     

        
    def ChartPredictions(self, forecast_set, forecasttarget):
        #Plot the Predictions
        last_date = self.dfData.iloc[-1].name
        last_unix = last_date
        next_unix = last_unix + datetime.timedelta(days=1)

        for i in forecast_set:
            next_date = next_unix
            next_unix += datetime.timedelta(days=1)
            self.dfData.loc[next_date] = [np.nan for _ in range(len(self.dfData.columns)-1)]+[i]
        
        self.dfData[self.TargetCol].tail(1000).plot()
        self.dfData[forecasttarget].tail(1000).plot()
        plt.legend(loc=4)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
        
        
    def CreateFeatureSets(self):
            self.X = self.dfData[self.FeatureCols].copy()
            print(self.X.head())
            print(self.X.tail())


    def ScaleFeatureSets(self):
        scaler = MinMaxScaler()
        self.X_scaled = scaler.fit_transform(self.X)
        self.X_scaled = pd.DataFrame(columns=self.FeatureCols, data=self.X_scaled, index=self.X.index)


    def CreateTargetSets(self):
        self.y = pd.DataFrame(self.dfData[self.TargetCol])


    def GenerateXTrainAndTestDataSets(self):
        self.training_begin = self.X.index.min()    
        timesplit= TimeSeriesSplit(n_splits=self.trainDataPercent)
        for train_index, test_index in timesplit.split(self.X_scaled):
            self.X_train, self.X_test = self.X_scaled[:len(train_index)], self.X_scaled[len(train_index): (len(train_index)+len(test_index))]
    
    
    def GenerateYTrainAndTestDataSets(self):
        self.training_begin = self.y.index.min()    
        timesplit= TimeSeriesSplit(n_splits=self.trainDataPercent)
        for train_index, test_index in timesplit.split(self.y):           
            self.y_train, self.y_test = self.y[:len(train_index)].values.ravel(), self.y[len(train_index): (len(train_index)+len(test_index))].values.ravel()


    def ExecuteSpecialModelRequirements(self):
        #Process the data for LSTM
        self.trainX = np.array(self.X_train)
        self.testX = np.array(self.X_test)
        self.X_special_train = self.trainX.reshape(self.X_train.shape[0], 1, self.X_train.shape[1])
        self.X_special_test = self.testX.reshape(self.X_test.shape[0], 1, self.X_test.shape[1])
    
    
    def PrepareModel(self):
        #Building the LSTM Model
        activation = 'linear'       #'softmax'  # 'relu', 'linear'
        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=(1, self.trainX.shape[1]), activation=activation, return_sequences=False))
        self.model.add(Dense(1))
        adamOpti = Adam(learning_rate = 0.00000001)
        self.model.compile(loss='mean_squared_error', optimizer=adamOpti)
        plot_model(self.model, show_shapes=True, show_layer_names=True)

    
    def FitModelToTrain(self):
        history = self.model.fit(self.X_special_train, self.y_train, epochs=100, batch_size=8, verbose=1, shuffle=False)


    def PredictTrain(self):
        self.y_pred = self.model.predict(self.X_special_test)

    
    def AnalyzePredictions(self):
        print(f'Printing Y Test {self.y_test}')
        print(f'Printing Y Pred {self.y_pred}')
        plt.plot(self.y_test, label='True Value')
        plt.plot(self.y_pred, label='LSTM Value')
        plt.title('Prediction by LSTM')
        plt.xlabel('Time Scale')
        plt.ylabel('Scaled USD')
        plt.legend()
        plt.show()


    def CreateModel(self, svmType):
        model = None
        if(svmType == "SVC"):
            model = svm.SVC()
        elif(svmType == "SVR"):
            model = svm.SVR()
        return model