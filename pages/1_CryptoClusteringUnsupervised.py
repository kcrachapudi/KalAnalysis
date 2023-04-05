
# Import required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from path import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import Utils
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import holoviews as hv

st.write(
"""
# KalAnalysis.com
Fun AI based Quant Stock and Crypto Analysis to analyze trends and predict outcomes.
"""
)


st.write(
"""
## Crypto Clustering
"""
)

"""
In this project we combine financial Python with unsupervised learning to help cluster Crypto Currencies.

The crypto currency data provided contains price change data of cryptocurrencies in different periods.

The steps for the analysis are broken out into the following sections:

* Import the Data 
* Prepare the Data 
* Find the Best Value for `k` Using the Original Data
* Cluster Cryptocurrencies with K-means Using the Original Data
* Optimize Clusters with Principal Component Analysis
* Find the Best Value for `k` Using the PCA Data
* Cluster the Cryptocurrencies with K-means Using the PCA Data
* Visualize and Compare the Results
"""


""" Import the Data
This section imports the data into a new DataFrame. It follows these steps:

1. Read  the crypto market data into a DataFrame and Review the DataFrame.

2. Generate the summary statistics, and use HvPlot to visualize your data to observe what your DataFrame contains.
"""

with st.spinner('Retrieving and loading Crypto Data...'):
    st.write("Load the data into a Pandas DataFram")
    df_market_data = Utils.GetCSVDataFromResources("crypto_market_data.csv", "coin_id")

    st.write('Display sample data')
    if df_market_data is not None:
        st.write(df_market_data.head(10))

        st.write('Generate summary statistics')
        st.write(df_market_data.describe())

        st.write('Plot the Dataframe Data')
        dfPlot = df_market_data.hvplot.line(
            height=600,
            rot=90,
            responsive=True
        )
        st.write(hv.render(dfPlot, backend='bokeh'))


        st.write('Prepare the Data')
        st.write(
        """
        This section prepares the data before running the K-Means algorithm. It follows these steps:

        1. Use the `StandardScaler` module from scikit-learn to normalize the CSV file data. This will require you to utilize the `fit_transform` function.

        2. Create a DataFrame that contains the scaled data. Be sure to set the `coin_id` index from the original DataFrame as the index for the new DataFrame. Review the resulting DataFrame.
        """)
        st.write(' Use the StandardScaler() module from scikit-learn to normalize the data from the CSV file')
        scaled_data = StandardScaler().fit_transform(df_market_data)
        st.write(' Create a DataFrame with the scaled data')
        df_market_data_scaled = pd.DataFrame(
            scaled_data,
            columns=df_market_data.columns
        )
        st.write(' Copy the crypto names from the original data')
        df_market_data_scaled["coin_id"] = df_market_data.index

        st.write(' Set the coinid column as index')
        df_market_data_scaled = df_market_data_scaled.set_index("coin_id")

        st.write(' Display sample scaled dataframe data')
        df_market_data_scaled.head()

        """
        ### Find the Best Value for k Using the Original Data
        In this section, you will use the elbow method to find the best value for `k`.

        1. Code the elbow method algorithm to find the best value for `k`. Use a range from 1 to 11. 

        2. Plot a line chart with all the inertia values computed with the different values of `k` to visually identify the optimal value for `k`.

        3. Answer the following question: What is the best value for `k`?
        """

        st.write(' Create a list with the number of k-values to try')
        st.write(' Use a range from 1 to 11')
        klist = list(range(1, 11))

        st.write(' Create an empy list to store the inertia values')
        inertias = []

        """
         Create a for loop to compute the inertia with each possible value of k
         Inside the loop:
         1. Create a KMeans model using the loop counter for the n_clusters
         2. Fit the model to the data using `df_market_data_scaled`
         3. Append the model.inertia_ to the inertia list
        """
        for i in klist:
            model = KMeans(n_clusters=i, random_state=0)
            model.fit(df_market_data_scaled)
            inertias.append(model.inertia_)

        st.write(' Create a dictionary with the data to plot the Elbow curve')
        elbow_dict = {
            "klist": klist,
            "inertias": inertias
        }

        st.write(' Create a DataFrame with the data to plot the Elbow curve')
        df_elbow = pd.DataFrame(elbow_dict)
        st.write(' Plot a line chart with all the inertia values computed with ')
        st.write(' the different values of k to visually identify the optimal value for k.')
        df_elbow_plot = df_elbow.hvplot.line(x="klist", y="inertias", title="Elbow Curve", xticks=klist, height=600, responsive=True)
        st.write(hv.render(df_elbow_plot, backend='bokeh'))

        st.write('#### Answer the following question: What is the best value for k?')
        st.write('**Question:** What is the best value for `k`?')
        st.write('**Answer:** The plot clearly shows that the best value of k is 4 as the the curve flattens out after that')

        st.write('### Cluster Cryptocurrencies with K-means Using the Original Data')
        """
        In this section, you will use the K-Means algorithm with the best value for `k` found in the previous section to cluster the cryptocurrencies according to the price changes of cryptocurrencies provided.

        1. Initialize the K-Means model with four clusters using the best value for `k`. 

        2. Fit the K-Means model using the original data.

        3. Predict the clusters to group the cryptocurrencies using the original data. View the resulting array of cluster values.

        4. Create a copy of the original data and add a new column with the predicted clusters.

        5. Create a scatter plot using hvPlot by setting `x="price_change_percentage_24h"` and `y="price_change_percentage_7d"`. Color the graph points with the labels found using K-Means and add the crypto name in the `hover_cols` parameter to identify the cryptocurrency represented by each data point.
         """
        st.write(' Initialize the K-Means model using the best value for k')
        model = KMeans(n_clusters=4)
        st.write(' Fit the K-Means model using the scaled data')
        model.fit(df_market_data_scaled)
        st.write(' Predict the clusters to group the cryptocurrencies using the scaled data')
        clusters = model.predict(df_market_data_scaled)

        st.write(' View the resulting array of cluster values.')
        print(clusters)
        st.write(' Create a copy of the DataFrame')
        df_market_data_scaled_predictions = df_market_data_scaled.copy()
        st.write(' Add a new column to the DataFrame with the predicted clusters')
        df_market_data_scaled_predictions['cluster'] = clusters
        st.write(' Display sample data')
        df_market_data_scaled_predictions.head()
        """ 
        Create a scatter plot using hvPlot by setting `x="price_change_percentage_24h"` and `y="price_change_percentage_7d"`. 
        Color the graph points with the labels found using K-Means and add the crypto name in the `hover_cols` parameter to identify the cryptocurrency represented by each data point.
        """
        df_market_data_scaled_predictions_plot = df_market_data_scaled_predictions.hvplot.scatter(x='price_change_percentage_24h', y='price_change_percentage_7d', by='cluster', hover_cols='coin_id', height=600, responsive=True, title='Scatter Plot by KMeans')
        st.write(hv.render(df_market_data_scaled_predictions_plot, backend='bokeh'))
