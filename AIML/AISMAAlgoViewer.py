from os import close
import streamlit as st
from fileinput import filename
import pandas as pd
from Intelligence import BackTestFinal, BackTestInitial, DataPreparer
import holoviews as hv
import numpy as np
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report
from enum import StrEnum
from Fin_AI_SMA_Algo import FinAISMAAlgo
from Utils import Helper, Utils


def View(algoml:FinAISMAAlgo, viewBasic=True, viewDetailed=False):
    #Create Features Set
    st.text_area(f'{algoml.UIComponentPrefix} Create the Features Set', " Think back to the dual moving average crossover (DMAC) trading algorithm that you generated in the previous lessons. You used a single trading signal to determine the entry and exit points for the algorithm. (That trading signal was the crossover point between the short-window and long-window SMAs.) The lesson demonstrations used the data to generate trading signals for holding long positions. By contrast, the activities used the trading signals to initiate short-position trades—first selling stock and then buying it to cover the sale, ideally at a lower price. For our machine learning–powered trading algorithm, the trading signals will make up the features set.")
    st.text_area(f'{algoml.UIComponentPrefix} ML2', f"Our new trading algorithm will continue to use the same short- and long-window SMA logic, but with a slight difference. We’ll create an SMA column using a window size of {algoml.short_window} days, and name it “sma_fast”. We’ll create another SMA column using a window size of {algoml.long_window} days, and name it sma_slow")
    st.write("We start by creating the sma_fast column in our DataFrame")
    st.write(' Create an SMA that uses short_window, and assign it to a new column named “sma_fast”')
    st.write('Similarly, we create the “sma_slow” column in our DataFrame')
    st.write('Create an SMA that uses long_window, and assign it to a new column named “sma_slow” ')
    st.write('Drop all the NaN values by using the dropna function')
    st.text_area(f'{algoml.UIComponentPrefix} ML3', "Finally, we create the X features set by copying the “sma_fast” and “sma_slow” columns from our original DataFrame into a new DataFrame named X. However, we want the model to learn a predictive relationship. (That is, we want to know how “sma_fast” and “sma_slow” will predict returns in the future.) We’ll thus use the shift function to shift the feature columns by 1. Doing so ensures that the model will use the current values to predict the outcome for the next period.")
    st.write('The following code creates the X features set and shifts the columns:')
    st.write(' Assign a copy of the `sma_fast` and `sma_slow` columns to a new DataFrame called X')
    st.write('Display X data')
    st.write(algoml.X.head())
    st.write(algoml.X.tail())

    #Create Target Sets
    st.text_area(f'{algoml.UIComponentPrefix} ML4 Create the Target Set', "Because we’ll use a supervised learning algorithm, we need to create a target set of the values that we want to predict. In this case, we’ll predict a signal that indicates whether we should buy or sell.For this trading algorithm, we’ll set the signals as follows: If the actual returns are equal to or greater than zero, we’re earning money. Therefore, the signal will indicate that we should buy a position, or go long, on the stock. By contrast, if the actual returns are less than zero, we’re starting to lose money. Therefore, we want to short the stock—that is, sell it with the intention of buying it later, at a lower price, to cover the sale.Let’s return to our original DataFrame and create a new column named “signal”. For now, this column will contain zeros, as the following code shows:")
    st.write('Create a new column in the dfTrades called "signal" setting its value to zero.')
    st.text_area(f'{algoml.UIComponentPrefix} ML5', 'Using the Pandas loc function, we evaluate whether the actual returns are positive, negative, or zero. Where the “actual_returns” value is greater than or equal to zero, we set the “signal” value to 1. Where the “actual_returns” value is less than zero, we set the “signal” value to −1, as the following code shows:')
    st.write(' Create the signal to buy')
    st.write('Create the signal to sell')
    st.write('Finally, we create the target set by copying the new “signal” column to a new Pandas Series named y, as the following code shows:')
    st.write(' Copy the new "signal" column to a new Series called `y`.')
    st.text_area(f'{algoml.UIComponentPrefix} ML6', 'The y target set now includes the target signals that we want to predict. A value of 1 indicates that the algorithm will buy stock. A value of −1 indicates that the algorithm will sell.Now that we have created the features and target sets, it’s time to split the data into training and testing datasets.')
    st.write(algoml.y)

    #GenerateXYTrainAndTestDataSets(algoml):
    st.text_area(f'{algoml.UIComponentPrefix} Split the Data into Training and Testing Sets', 'As we did with machine learning models in previous modules, we’ll split the prepared data into training and testing sets. We’ll use the training data to train the machine learning model to make buy and sell predictions. We’ll use the testing data to backtest the trained model—to find out how well it performs at algorithmic trading.Rather than using train_test_split from scikit-learn to create the training and testing sets, as we did in the previous modules, we’ll split the data into training and testing sets by using date windows.')
    st.text_area(f'{algoml.UIComponentPrefix} Import the DateOffset Module', f'For this demo, our training data will contain only a portion of the entire dataset—specifically, {algoml.trainDataPeriodmonths} months’ worth. We therefore need to create a date offset of {algoml.trainDataPeriodmonths} months. To do so, we first need to import the DateOffset module from pandas.tseries.offsets, as the following code shows:')

    st.text_area(f'{algoml.UIComponentPrefix} Create the Training Datasets', f'To define the training datasets, we need to define where we want the training data values to begin and end. We first define two new variables: training_begin and training_end. We use the Pandas index.min function to set the value of training_begin to the minimum index value in the X features DataFrame. We use the DateOffset module to set the value of training_end to the minimum index value plus a date offset of {algoml.trainDataPeriodmonths} months, as the following code shows:')
    st.write('Select the start of the training period')
    st.write(f'Training_begin Date {algoml.training_begin}')
    st.write(f'Select the ending period for the training data with an offset of {algoml.trainDataPeriodmonths} months')
    st.write(f'Training_end Date {algoml.training_end}')

    st.write('Now, we can generate our X_train and y_train datasets by using the loc function with our training_begin and training_end values, as the following code shows:')
    st.write('Generate the X_train and y_train DataFrames')
    st.write('Display X_train data')
    st.write(algoml.X_train.head())
    st.text_area(f'{algoml.UIComponentPrefix} ML7','In the preceding notice that the first row in the X_train DataFrame includes an index value which matches the value of the training_begin variable. The row also includes values for "sma_fast" and "sma_slow".')
    st.text_area(f'{algoml.UIComponentPrefix} Create the Testing Datasets','We similarly create our testing datasets. The only difference when we create the X_test and y_test DataFrames occurs when we slice the data. We slice the index starting at the training_end value and ending at the last record of the datasets, as the following code shows:')
    st.write('Generate the X_test and y_test DataFrames')
    st.write('Display sample X_test data')
    st.write(algoml.X_test.head())

    #ScaleDataSets(algoml):
    st.text_area(f'{algoml.UIComponentPrefix} ML8 Standardize the Data', 'With our training and testing datasets in place, the next step is to standardize the data in the X_train and X_test DataFrames by using the StandardScaler module from scikit-learn.Right now, the values of our features (that is, the X data values that we’ll use to make predictions) aren’t standardized. If certain “sma_fast” and “sma_slow” values are very high, that might skew our model’s ability to develop accurate predictions. So, like with most machine learning applications, we should first standardize, or scale, our feature data.')
    st.write('We can standardize data by subtracting the average from each feature and then dividing by the standard deviation of the feature.')
    st.text_area(f'{algoml.UIComponentPrefix} ML9','As before, we use the StandardScaler module to transform our X_train and X_test datasets. To do so, we import the StandardScaler module from sklearn.preprocessing, instantiate a new StandardScaler instance, and then fit it to our X_train dataset, as the following code shows:')
    st.write('Import the required module -> from sklearn.preprocessing import StandardScaler')
    st.write('Create a StandardScaler instance')
    st.write('Apply the scaler model to fit the X_train data')
    st.write('Transform the X_train and X_test DataFrames using the X_scaler')
    st.text_area(f'{algoml.UIComponentPrefix} ML10','Our feature data is now standardized, so any outlier data points shouldn’t influence the machine learning model. With our data finally prepared and ready to go, it’s now time to incorporate the machine learning model into our trading strategy.')

    #FitModelToTrain(algoml):
    st.text_area(f'{algoml.UIComponentPrefix} Use Machine Learning in a Trading Strategy',f'In this section, we use our training data to fit a machine learning model to predict the target trading signal. For this demonstration, we use the {algoml.modelType} learning methodLinks to an external site. from SKLearn, and its modelLinks to an external site.. The reason is its ability to discriminate between two classes, and we want to predict whether the signal will be 1 or −1.The following code imports from SKLearn:')
    st.write(f' Import the {algoml.UIComponentPrefix} model')
    st.write('We now fit the model to the X_train_scaled and y_train data. As we’ve noted with other machine learning models, the model learns from the training dataset and makes predictions based on the testing dataset, which is X_test_scaled in this case.')
    st.write('The training_signal_predictions variable will contain our predicted values, which will exist in an array of buy and sell values.')
    st.write('The following code fits the model:')
    st.write('Create the classifier model')
    st.write('Fit the model to the data using X_train_scaled and y_train')

    #PredictTrain(algoml):
    st.write(' Use the trained model to predict the trading signals for the training data')
    st.write('Display the sample training signal predictions')
    st.write(algoml.TrainingSignalPredictions[:10])
    st.write('Now that we have generated predictions from our training data, we evaluate the results by using the clasification_report module from scikit-learn, as the following code shows:')
    st.write('Import the required module -> from sklearn.metrics import classification_report')
    st.write('Evaluate the model using a classification report')
    st.write(f'Training Classification Report {algoml.TrainingClassificationReport}')
    st.write(f'Rounded Training Classification Report {algoml.TrainingClassificationReport}')
    st.write("Training Report Details")
    st.write(algoml.dfTrainingReport)
    st.write(f'The precision is {algoml.dfTrainingReport.loc["precision"][algoml.BuySignalKey]} for the {algoml.BuySignalKey} class and {algoml.dfTrainingReport.loc["precision"][algoml.SellSignalKey]} for the {algoml.SellSignalKey} class.')
    st.write(f'The recall is {algoml.dfTrainingReport.loc["recall"][algoml.BuySignalKey]} for the {algoml.BuySignalKey} class and {algoml.dfTrainingReport.loc["recall"][algoml.SellSignalKey]} for the {algoml.SellSignalKey} class.')

    #PredictTest(algoml):
    st.text_area(f'{algoml.UIComponentPrefix} Backtest a Machine Learning Trading Algorithm','Before putting a model to work with new data, it’s important to test it. With backtesting, we can assess the performance of a trading strategy by using historical data to find out how the model would have performed in the past.The theory behind backtesting a model is that if the model can accurately predict outcomes by using historical data, it will perform well with current data. You can learn more about backtesting from the Investopedia articles BacktestingLinks to an external site. and The Importance of Backtesting Trading StrategiesLinks to an external site..')
    st.write('To backtest our model, we use the trained model to predict the trading signals for the testing data, as the following code shows:')
    st.write('Use the trained model to predict the trading signals for the testing data.')
    st.write('Display the sample testing signal predictions')
    st.write(algoml.TestingSignalPredictions[:10])
    st.write('Now, we evaluate the ability of the model to make predictions by using a classification report, as the following code shows:')
    st.write('Evaluate the models ability to predict the trading signal for the testing data')
    st.write(f'Testing Classification Report {algoml.TestingClassificationReport}')
    st.write(f'Rounded Testing Classification Report {algoml.TestingClassificationReport}')
    st.write("Testing Report Details")
    st.write(algoml.dfTestingReport)
    st.write(f'The precision is {algoml.dfTestingReport.loc["precision"][algoml.BuySignalKey]} for the {algoml.BuySignalKey} class and {algoml.dfTestingReport.loc["precision"][algoml.SellSignalKey]} for the {algoml.SellSignalKey} class.')
    st.write(f'The recall is {algoml.dfTestingReport.loc["recall"][algoml.BuySignalKey]} for the {algoml.BuySignalKey} class and {algoml.dfTestingReport.loc["recall"][algoml.SellSignalKey]} for the {algoml.SellSignalKey} class.')
    
    #AnalyzeClassificationReports(algoml):
    st.write(f'Compare the recall for the {algoml.BuySignalKey} class of the training data ({algoml.dfTrainingReport.loc["recall"][algoml.BuySignalKey]} vs. {algoml.dfTestingReport.loc["recall"][algoml.BuySignalKey]}')
    st.write(f'Compare the recall for the {algoml.SellSignalKey} class of the testing data ({algoml.dfTrainingReport.loc["recall"][algoml.SellSignalKey]} vs. {algoml.dfTestingReport.loc["recall"][algoml.SellSignalKey]}.')
    st.write(f'The accuracy score comparison for the recall training data is {algoml.dfTrainingReport.loc["recall"]["accuracy"]} and for testing data is {algoml.dfTestingReport.loc["recall"]["accuracy"]}.')
    st.text_area(f'{algoml.UIComponentPrefix} Compare the Actual and Predicted Returns',f'From the classification reports, we can observe that the accuracy of the model is about 0.50, or 50%.')

    #AnalyzePredictions(algoml):
    st.write('For a different perspective on the model’s performance, we’ll create a plot to visually compare the actual and predicted returns.Let’s start by creating a new DataFrame with the actual and predicted returns, as the following code shows:')
    st.write('Create a predictions DataFrame')
    st.write(algoml.dfPredictions.head())
    st.write(algoml.dfPredictions.tail())
    st.text_area(f'{algoml.UIComponentPrefix} ML14', f'Notice that the DataFrame has “predicted_signal”, “actual_returns”, and “trading_algorithm_returns” columns.')

    #AnalyzePredictionsPlot(algoml):
    st.write('Let us plot the cumulative returns and compare the actual returns to those that our model predicted by using the historical data.')
    st.write("Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns` ")
    st.write('cumprod -> (1 + dfPredictions[["actual_returns", "trading_algorithm_returns"]]).cumprod()')
    st.write(hv.render(algoml.cumprodplot1, backend='bokeh'))
    st.write(hv.render(algoml.cumprodplot2, backend='bokeh'))
    st.text_area(f'{algoml.UIComponentPrefix} ML15', 'Notice that our SVM model performed well from the beginning of the period until early in 2020. That’s when the actual and predicted returns start to greatly differ. To truly find out how well this model works, however, we need to fit it to different sets of pricing data, have it make predictions, backtest it, and then evaluate it against the actual performance of the asset with that trading strategy. backtesting the SMA long-short trading strategy using the SVM model provides an interesting example of the predictive power of machine learning. The SVM model made trading decisions that strongly outperformed the actual returns in some market scenarios, as illustrated by the steep rise in the trading_algorithm_returns plot line. However, sometimes the SVM model also made decisions that underperformed relative to the actual returns, as illustrated by the steep decline in the trading_algorithm_returns plot line. Overall, the SVM models trading decisions, though more volatile, produced a higher cumulative return value than the original trading strategys actual returns.')
