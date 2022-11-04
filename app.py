import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import main
import Utils

"""
# KalAnalysis.com!
Comprehensive AI based Quant Stock Analysis to empower Users to make informed Trade Decisions.
"""

""

CURRENT_THEME = "blue"
IS_DARK_THEME = True

dfTickersList = None
dfTickers = None
dfTicker = None
dfTickersGrid = None 
lstTickers = []

finalTicker = None

def GetTickersFromCSV():
    dfData = None
    try:
        dfData = pd.read_csv('Tickers.csv')
        st.write("## THE DATA BEING USED")
    except Exception as ex:
        print(f"Error in Loading Tickers.csv {ex}")
    return dfData

# Draw some dummy content in main page and sidebar.
def drawSidebar(
    key,
    plot=False,
):
    st.write("Fun and educative Stock Analysis!")

def drawMain(key, plot=False,):
    tabTickers, tabTickers2, tabThemes, tabHeader, tab1, tab2, tab3, tabPlots = st.tabs(["Tickers", "Tickers2", 'Themes', 'Header', "Tab1", "Tab2", "Tab3", 'Plots'])
    with tabTickers:
        dfTickersList = GetTickersFromCSV()
        #AgGrid(dfTickerData)

        gb = GridOptionsBuilder.from_dataframe(dfTickersList)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        gridOptions = gb.build()

        grid_response = AgGrid(
            dfTickersList,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            #theme='blue', #Add theme color to the table
            enable_enterprise_modules=True,
            height=350, 
            width='100%',
            reload_data=False
        )
        data = grid_response['data']
    with tabTickers2:
        st.header("Analyze Tickers")       
        st.table(dfTickersList)
    with tabThemes:
        THEMES = [
            "light",
            "dark",
            "green",
            "blue",
        ]
        GITHUB_OWNER = "streamlit"
        EXPANDER_TEXT = """
            This is a custom theme. You can enable it by copying the following code
            to `.streamlit/config.toml`:

            ```python
            [theme]
            primaryColor = "#E694FF"
            backgroundColor = "#00172B"
            secondaryBackgroundColor = "#0083B8"
            textColor = "#C6CDD4"
            font = "sans-serif"
            ```
            """

        # Show thumbnails for available themes.
        # As html img tags here, so we can add links on them.
        cols = st.beta_columns(len(THEMES))
        for col, theme in zip(cols, THEMES):

            # Get repo name for this theme (to link to correct deployed app)-
            if theme == "light":
                repo = "theming-showcase"
            else:
                repo = f"theming-showcase-{theme}"

            # Set border of current theme to red, otherwise black or white
            if theme == CURRENT_THEME:
                border_color = "red"
            else:
                border_color = "lightgrey" if IS_DARK_THEME else "black"

            col.markdown(
                #f'<p align=center><a href="https://share.streamlit.io/{GITHUB_OWNER}/{repo}/main"><img style="border: 1px solid {border_color}" alt="{theme}" src="https://raw.githubusercontent.com/{GITHUB_OWNER}/theming-showcase/main/thumbnails/{theme}.png" width=150></a></p>',
                f'<p align=center><a href="https://apps.streamlitusercontent.com/{GITHUB_OWNER}/{repo}/main/streamlit_app.py/+/"><img style="border: 1px solid {border_color}" alt="{theme}" src="https://raw.githubusercontent.com/{GITHUB_OWNER}/theming-showcase/main/thumbnails/{theme}.png" width=150></a></p>',
                unsafe_allow_html=True,
            )
            if theme in ["light", "dark"]:
                theme_descriptor = theme.capitalize() + " theme"
            else:
                theme_descriptor = "Custom theme"
            col.write(f"<p align=center>{theme_descriptor}</p>", unsafe_allow_html=True)


        ""
        with st.beta_expander("Not loading?"):
            st.write(
                "You probably played around with themes before and overrode this app's theme. Go to ☰ -> Settings -> Theme and select *Custom Theme*."
            )
        with st.beta_expander("How can I use this theme in my app?"):
            st.write(EXPANDER_TEXT)

        ""
        ""
    with tabHeader:
        # This code is different for each deployed app.
        st.image(
            "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/artist-palette_1f3a8.png",
            width=100,
        )
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab3:
        # st.header("An owl")
        # st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
        # st.file_uploader("You can now upload with style", key=key)
        # st.slider(
        #     "From 10 to 11, how cool are themes?", min_value=10, max_value=11, key=key
        # )
        # # st.select_slider("Pick a number", [1, 2, 3], key=key)
        # st.number_input("So many numbers", key=key)
        # st.text_area("A little writing space for you :)", key=key)
        # st.selectbox(
        #     "My favorite thing in the world is...",
        #     ["Streamlit", "Theming", "Baloooons 🎈 "],
        #     key=key,
        # )
        # # st.multiselect("Pick a number", [1, 2, 3], key=key)
        # # st.color_picker("Colors, colors, colors", key=key)
        # with st.beta_expander("Expand me!"):
        #     st.write("Hey there! Nothing to see here 👀 ")
        # st.write("")
        # # st.write("That's our progress on theming:")
        # # st.progress(0.99)
        # if plot:
        #     st.write("And here's some data and plots")
        #     st.json({"data": [1, 2, 3, 4]})
        #     st.dataframe({"data": [1, 2, 3, 4]})
        #     st.table({"data": [1, 2, 3, 4]})
        #     st.line_chart({"data": [1, 2, 3, 4]})
        #     # st.help(st.write)
        st.write("This is the end. Have fun building themes!")
    with tabPlots:
        st.write(
            """
           
            Please select the Tickers below for analysis 👀 
        
            ```python
            # First some code.
            streamlit = "cool"
            theming = "fantastic"
            both = "💥"
            ```
            """
        )
    
        # if plot:
        #     st.write("Oh look, a plot:")
        #     x1 = np.random.randn(200) - 2
        #     x2 = np.random.randn(200)
        #     x3 = np.random.randn(200) + 2

        #     hist_data = [x1, x2, x3]
        #     group_labels = ["Group 1", "Group 2", "Group 3"]

        #     fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

        #     st.plotly_chart(fig, use_container_width=True)
        st.header("Sample Plots")

    if st.button('Download Tickers Data'):
        st.write(f'Downloading data for Selected Tickers')
        if(grid_response['selected_rows'] is not None and len(grid_response['selected_rows'])>0):
            for rowticker in grid_response['selected_rows']:
                lstTickers.append(rowticker["Ticker"])
            dfTickers = main.LoadTickersData(lstTickers)

    st.header("Symbol Analysis - SA")    
    selTicker = st.multiselect('Select Ticker to Analyze', lstTickers)
    st.write('Selected Ticker :', selTicker)
    tabSADetails, tabSADetailsRaw = st.tabs(["Symbol Details", "Raw Details"])
    with tabSADetails:
        try:
            if(selTicker is not None):
                st.header(f"Ticker {selTicker} Data") 
                dfTicker = main.GetTickerData(selTicker)      
                gb1 = GridOptionsBuilder.from_dataframe(dfTicker)
                gb1.configure_pagination(paginationAutoPageSize=True) #Add pagination
                gb1.configure_side_bar() #Add a sidebar
                gb1.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
                gb1.configure_column("Date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
                gridOptions1 = gb1.build()

                grid_response1 = AgGrid(
                    dfTickersGrid,
                    gridOptions=gridOptions1,
                    data_return_mode='AS_INPUT', 
                    update_mode='MODEL_CHANGED', 
                    fit_columns_on_grid_load=False,
                    #theme='blue', #Add theme color to the table
                    enable_enterprise_modules=True,
                    height=350, 
                    width='100%',
                    reload_data=False
                )

                data = grid_response1['data']
                selected1 = grid_response1['selected_rows'] 
                dfSelected1 = pd.DataFrame(selected1) #Pass the selected rows to a new dataframe df    
        except:    
            st.write(f"Ticker not selected")       
    with tabSADetailsRaw:
        try:
            if(ticker is not None):
                st.header(f"Ticker {ticker} Data")       
                st.table(dfTickers)
        except:    
            st.write(f"Ticker not selected")       


drawMain("main", plot=True)

with st.sidebar:
    drawSidebar("sidebar")