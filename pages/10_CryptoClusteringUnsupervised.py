
# Import required libraries and dependencies
import streamlit as st
from fileinput import filename
import pandas as pd
import hvplot.pandas
from path import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from Intelligence import Utils
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


        st.write('### Optimize Clusters with Principal Component Analysis')
        """
        In this section, you will perform a principal component analysis (PCA) and reduce the features to three principal components.

        1. Create a PCA model instance and set `n_components=3`.

        2. Use the PCA model to reduce to three principal components. View the first five rows of the DataFrame. 

        3. Retrieve the explained variance to determine how much information can be attributed to each principal component.

        4. Answer the following question: What is the total explained variance of the three principal components?

        5. Create a new DataFrame with the PCA data. Be sure to set the `coin_id` index from the original DataFrame as the index for the new DataFrame. Review the resulting DataFrame.
        """
        st.write(' Create a PCA model instance and set `n_components=3`.')
        pca = PCA(n_components=3)
        st.write(' Use the PCA model with `fit_transform` to reduce to three principal components.')
        pca_data = pca.fit_transform(df_market_data_scaled)
        st.write(' View the first five rows of the DataFrame. ')
        pca_data[:5]
        st.write(' Retrieve the explained variance to determine how much information can be attributed to each principal component.')
        pca.explained_variance_ratio_
        total_explained_variance = round(sum(pca.explained_variance_ratio_)*100, 2)
        st.write('total_explained_variance is {total_explanied_variance}')
        st.write('#### Answer the following question: What is the total explained variance of the three principal components?')
        st.write('**Question:** What is the total explained variance of the three principal components?')
        st.write('**Answer:** The total explained variance of the three principal components is 89.5%')
        st.write(' Creating a DataFrame with the PCA data')
        df_market_data_pca = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2', 'PCA3'])
        st.write(' Copy the crypto names from the original data')
        df_market_data_pca['coin_id'] = df_market_data.index
        st.write(' Set the coinid column as index')
        df_market_data_pca = df_market_data_pca.set_index('coin_id')
        st.write(' Display sample data')
        st.write(df_market_data_pca.head())
        st.write('### Find the Best Value for k Using the PCA Data')
        """
        In this section, you will use the elbow method to find the best value for `k` using the PCA data.

        1. Code the elbow method algorithm and use the PCA data to find the best value for `k`. Use a range from 1 to 11. 

        2. Plot a line chart with all the inertia values computed with the different values of `k` to visually identify the optimal value for `k`.

        3. Answer the following questions: What is the best value for k when using the PCA data? Does it differ from the best k value found using the original data?
        """
        st.write(' Create a list with the number of k-values to try Use a range from 1 to 11')
        k2list = list(range(1, 11))
        st.write(' Create an empy list to store the inertia values')
        inertias2 = []
        st.write(' Create a for loop to compute the inertia with each possible value of k')
        """ Inside the loop:
         1. Create a KMeans model using the loop counter for the n_clusters
         2. Fit the model to the data using `df_market_data_pca`
         3. Append the model.inertia_ to the inertia list
        """
        for i in k2list:
            model = KMeans(n_clusters=i, random_state=0)
            model.fit(df_market_data_pca)
            inertias2.append(model.inertia_)

        st.write(' View the inertia list')
        st.write(inertias2)
        st.write(' Create a dictionary with the data to plot the Elbow curve')
        elbow2_data = {
            "k2list": k2list, 
            "inertias2": inertias2
        }
        st.write('  Create a DataFrame with the data to plot the Elbow curve')
        df_elbow2 = pd.DataFrame(elbow2_data)
        st.write(' Plot a line chart with all the inertia values computed with the different values of k to visually identify the optimal value for k.')
        df_elbow2_plot = df_elbow2.hvplot.line(x="k2list", y="inertias2", title="Elbow Curve", xticks=k2list, height=500, responsive=True)
        st.write(hv.render(df_elbow2_plot, backend='bokeh'))
        st.write(' #### Answer the following questions: What is the best value for k when using the PCA data? Does it differ from the best k value found using the original data?')
        """***Question:** What is the best value for `k` when using the PCA data?')
        * **Answer:** The best value for k when using the PCA data is 4
        * **Question:** Does it differ from the best k value found using the original data?
        * **Answer:** The best value for k in this situation does not differ from the k value found using the original data. 
        """

        st.write(' ### Cluster Cryptocurrencies with K-means Using the PCA Data')
        """"
        In this section, you will use the PCA data and the K-Means algorithm with the best value for `k` found in the previous section to cluster the cryptocurrencies according to the principal components.
        1. Initialize the K-Means model with four clusters using the best value for `k`. 
        2. Fit the K-Means model using the PCA data.
        3. Predict the clusters to group the cryptocurrencies using the PCA data. View the resulting array of cluster values.
        4. Add a new column to the DataFrame with the PCA data to store the predicted clusters.
        5. Create a scatter plot using hvPlot by setting `x="PC1"` and `y="PC2"`. Color the graph points with the labels found using K-Means and add the crypto name in the `hover_cols` parameter to identify the cryptocurrency represented by each data point.
        """
        st.write(' Initialize the K-Means model using the best value for k')
        model2 = KMeans(n_clusters=4)
        st.write(' Fit the K-Means model using the PCA data')
        model2.fit(df_market_data_pca)
        st.write(' Predict the clusters to group the cryptocurrencies using the PCA data')
        pcaclusters = model2.predict(df_market_data_pca)
        st.write(' View the resulting array of cluster values.')
        st.write(pcaclusters)
        st.write(' Create a copy of the DataFrame with the PCA data')
        df_market_data_pca_predictions = df_market_data_pca.copy()
        st.write(' Add a new column to the DataFrame with the predicted clusters')
        df_market_data_pca_predictions['cluster'] = pcaclusters
        st.write(' Display sample data')
        df_market_data_pca_predictions.head()
        st.write(' Create a scatter plot using hvPlot by setting ')
        st.write(' x="PC1"` and y="PC2"`. Color the graph points with the labels found using K-Means and add the crypto name in the `hover_cols` parameter to identify the cryptocurrency represented by each data point.')
        df_market_data_pca_predictions_plot = df_market_data_pca_predictions.hvplot.scatter(x='PCA1', y='PCA2', by='cluster', title='Scatter Plot by PCA Clusters', hover_cols='coin_id', height=500, responsive=True)
        st.write(hv.render(df_market_data_pca_predictions_plot, backend='bokeh'))

        st.write('### Visualize and Compare the Results')
        """
        In this section, you will visually analyze the cluster analysis results by contrasting the outcome with and without using the optimization techniques.
        1. Create a composite plot using hvPlot and the plus (`+`) operator to contrast the Elbow Curve that you created to find the best value for `k` with the original and the PCA data.
        2. Create a composite plot using hvPlot and the plus (`+`) operator to contrast the cryptocurrencies clusters using the original and the PCA data.
        3. Answer the following question: After visually analyzing the cluster analysis results, what is the impact of using fewer features to cluster the data using K-Means?
        > You can look at that lesson to review how to make these plots; also, you can check [the hvPlot documentation](https://holoviz.org/tutorial/Composing_Plots.html).
        """
        st.write('Composite plot to contrast the Elbow curves')
        st.write(hv.render(df_elbow_plot + df_elbow2_plot, backend='bokeh'))
        #df_elbow_plot + df_elbow2_plot
        st.write(' Compoosite plot to contrast the clusters')
        st.write(hv.render(df_market_data_scaled_predictions_plot + df_market_data_pca_predictions_plot, backend='bokeh'))
        #df_market_data_scaled_predictions_plot + df_market_data_pca_predictions_plot
        """
        #### Answer the following question: After visually analyzing the cluster analysis results, what is the impact of using fewer features to cluster the data using K-Means?
        * **Question:** After visually analyzing the cluster analysis results, what is the impact of using fewer features to cluster the data using K-Means?
        * **Answer:** After visually analyzing the cluster analysis results using the PCA method with fewer features clearly shows that the PCA Plot is much better and shows clearly identifed Clusters
        """