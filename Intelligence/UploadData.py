import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import base64
from Utils.CSVReader import ETLCSVtoDataFrame
from Utils.Weber import download_link


def upload_data():
    st.markdown("""
    ## Data Insight & Modeling Assistant:
    This dynamic application serves as your companion in the realm of data science and business analytics. Crafted with simplicity and efficiency in mind, it aims to bridge the gap between raw data and actionable insights. Whether you're a seasoned data scientist, a business analyst seeking to uncover trends, or a student diving into the world of data, this tool is designed to cater to your needs.


    ### Designed for Ease and Insight:
    
    Our goal is to make data analysis accessible and insightful. With a focus on user experience, this app guides you through each step of the data science process, from initial data upload to deep analysis. Whether your project is aimed at predicting trends, classifying outcomes, or simply exploring data, our platform is equipped to provide the insights you need.

    Embrace the power of data with a tool that simplifies complexity and illuminates the path from data to decision. Explore, analyze, model, and achieve your data science endeavors with confidence.

  

    
    """)

    # Dataset options for dropdown
    dataset_options = {
        'Select a Dataset': None,
        'IRIS Dataset (Clustering & Feature Selection)': 'Data/IRIS.csv',
        'Churn Dataset (Classification Analysis)': 'Data/churn.csv',
        'Decision Tree Classifier Dataset (Will Buy)': 'Data/DTClassiferWillBuy.csv',
        'Decision Tree Regression Dataset (Loan Amount)': 'Data/DTRegressionLoan.csv',
        'Park Data (Time Series ARIMA Analysis)': 'Data/ParkData_5years.csv',
        'Airbnb Dataset (Price Regression & Causality)': 'Data/df_selected1.csv',
        'Uncleaned Airbnb File (Data Cleaning & Exploration)': 'Data/listing.csv'
    }

    # Dropdown for dataset selection
    selected_dataset = st.selectbox('Want to explore?  We have these datasets ready to preload!', list(dataset_options.keys()))

    if selected_dataset != 'Select a Dataset':
        dataset_path = dataset_options[selected_dataset]
        st.session_state.data = pd.read_csv(dataset_path)
        st.write(f"{selected_dataset.split('(')[0].strip()} loaded:")
        st.write(st.session_state.data.head())

    # Option to clear the preloaded or uploaded file
    if st.button('Clear Data'):
        st.session_state.data = None
        st.write("Data cleared. You can now upload your own dataset or choose another from the dropdown.")

    # Step 1: Upload CSV
    uploaded_file = st.file_uploader("Or upload your CSV file", type="csv")

    if uploaded_file:
        #st.session_state.data = pd.read_csv(uploaded_file)
        st.session_state.data = ETLCSVtoDataFrame(uploaded_file, 'bytes')

        st.write("Uploaded data preview:")
        st.write(st.session_state.data)

    # Provide a button for users to download the dataframe
    if 'data' in st.session_state and st.session_state.data is not None:
        if st.button('Download Dataframe as CSV'):
            tmp_download_link = download_link(st.session_state.data, 'your_data.csv', 'Click here to download the data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

    