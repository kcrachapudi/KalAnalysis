import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import Home
import Utils
import Models
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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



def GetTickersFromCSV():
    dfData = None
    try:
        dfData = pd.read_csv('Tickers.csv')
        st.write("## THE DATA BEING USED")
    except Exception as ex:
        print(f"Error in Loading Tickers.csv {ex}")
    return dfData


def init(key, plot=False,):
    if 'selTicker' not in st.session_state: 
        st.session_state.selTicker = None
    if 'finalTicker' not in st.session_state: 
        st.session_state.finalTicker = None
    if 'lstTickers' not in st.session_state:
        st.session_state.lstTickers = []
    if 'company' not in st.session_state: 
        st.session_state.company = None

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

        #     st.session_state.company_data = [x1, x2, x3]
        #     group_labels = ["Group 1", "Group 2", "Group 3"]

        #     fig = ff.create_distplot(st.session_state.company_data, group_labels, bin_size=[0.1, 0.25, 0.5])

        #     st.plotly_chart(fig, use_container_width=True)
        st.header("Sample Plots")

    if st.button('Download Tickers Data'):
        st.write(f'Downloading data for Selected Tickers')
        if(grid_response['selected_rows'] is not None and len(grid_response['selected_rows'])>0):
            for rowticker in grid_response['selected_rows']:
                print(f'row ticker of ticker  is {rowticker["Ticker"]}')
                st.session_state.lstTickers.append(rowticker["Ticker"])
            dfTickers = Home.LoadTickersData(st.session_state.lstTickers)
            print(f'lstTickers is {st.session_state.lstTickers}')

    st.header("Symbol Analysis - SA")    
    def TickerSelected():
        print(f'Selected Ticker :{st.session_state.selTicker}')
        #st.write(f'Selected Ticker :{selTicker}')
    st.session_state.selTicker = st.selectbox('Select Ticker to Analyze', options=st.session_state.lstTickers)
    print(st.session_state.selTicker)
    if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
        st.session_state.company = Home.GetCompanyDetails(st.session_state.selTicker)      
    
    tabTickerData, tabCloseData, tabVolumeData, tabCloseVolumeData, tabOHLC = st.tabs(["Ticker Data", 'Close Data', 'Volume Data', 'CloseAndVolume', 'OHLC'])
    with tabTickerData:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                st.header(f"Ticker {st.session_state.selTicker} Data") 
                #st.table(st.session_state.company.dfCompany)
                st.dataframe(st.session_state.company.dfCompany, 700, 300)
        except Exception as ex:    
            st.write(f"Exception {ex}")               
    with tabCloseData:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                st.header(f"{st.session_state.selTicker} Close Data") 
                dfClose = st.session_state.company.dfCompany['Close']
                st.dataframe(dfClose, 700, 300)

                chtClosest.session_state.company = go.Figure(data=go.Scatter(x=dfClose.index, y=dfClose, mode='lines'))
                #chtClosest.session_state.company.show() This shows a plot in a new browser tab
                st.plotly_chart(chtClosest.session_state.company, use_container_width=True)

                chtClosest.session_state.company1 = go.Figure(data=go.Scatter(x=dfClose.index, y=dfClose, mode='lines+markers'))
                st.plotly_chart(chtClosest.session_state.company1, use_container_width=True)
        except Exception as ex1:    
            st.write(f"Exception {ex1}")       
    with tabVolumeData:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                st.header(f"{st.session_state.selTicker}  Volume Data") 
                dfVolume = st.session_state.company.dfCompany['Volume']
                st.dataframe(dfVolume, 700, 300)

                chtVolumest.session_state.company = go.Figure(data=go.Scatter(x=dfVolume.index, y=dfVolume, mode='lines'))
                st.plotly_chart(chtVolumest.session_state.company, use_container_width=True)

                chtVolumest.session_state.company1 = go.Figure(data=go.Scatter(x=dfVolume.index, y=dfVolume, mode='lines+markers'))
                st.plotly_chart(chtVolumest.session_state.company1, use_container_width=True)        
        except Exception as ex2:    
            st.write(f"Exception {ex2}")       
    with tabCloseVolumeData:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                st.header(f"{st.session_state.selTicker}  Close and Volume") 
                dfClose = st.session_state.company.dfCompany['Close']
                dfVolumne = st.session_state.company.dfCompany['Volume']

                chtCloseVolume1 = make_subplots(specs=[[{"secondary_y": True}]])
                chtCloseVolume1.add_trace(go.Scatter(x=dfClose.index, y=dfClose, name='Close'), secondary_y=False)
                chtCloseVolume1.add_trace(go.Bar(x=dfVolume.index, y=dfVolume, name='Volume'), secondary_y=True)
                st.plotly_chart(chtCloseVolume1, use_container_width=True)

                chtCloseVolume2 = make_subplots(specs=[[{"secondary_y": True}]])
                chtCloseVolume2.add_trace(go.Scatter(x=dfClose.index, y=dfClose, name='Close'), secondary_y=False)
                chtCloseVolume2.add_trace(go.Bar(x=dfVolume.index, y=dfVolume, name='Volume'), secondary_y=True)
                chtCloseVolume2.update_yaxes(range=[0,70000000],secondary_y=True)
                chtCloseVolume2.update_yaxes(visible=False, secondary_y=True)
                st.plotly_chart(chtCloseVolume2, use_container_width=True)
        except Exception as ex2:    
            st.write(f"Exception {ex2}")       
    with tabOHLC:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                st.header(f"{st.session_state.selTicker}  OHLC") 
                chtOHLC = make_subplots(specs=[[{"secondary_y": True}]])
                chtOHLC.add_trace(go.Candlestick(x=st.session_state.company.dfCompany.index,
                              open=st.session_state.company.dfCompany['Open'],
                              high=st.session_state.company.dfCompany['High'],
                              low=st.session_state.company.dfCompany['Low'],
                              close=st.session_state.company.dfCompany['Close'],
                             ))
                st.plotly_chart(chtOHLC, use_container_width=True)
        except Exception as ex3:
            st.write(f"Exception {ex3}")               

    #Indicators and Analytics
    st.header(f"{st.session_state.selTicker} Indicators") 
    tabIndicator20, tabIndicator60, tabIndicator180, tabIndicator360 = st.tabs(["20 Day Moving Average", '60 Day Moving Average', '180 Day Moving Average', '360 Day Moving Average'])
    with tabIndicator20:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                chtInd20MA = make_subplots(specs=[[{"secondary_y": True}]])
                chtInd20MA.add_trace(go.Candlestick(x=st.session_state.company.dfCompany.index,
                                            open=st.session_state.company.dfCompany['Open'],
                                            high=st.session_state.company.dfCompany['High'],
                                            low=st.session_state.company.dfCompany['Low'],
                                            close=st.session_state.company.dfCompany['Close'],
                                            name='Price'))
                chtInd20MA.add_trace(go.Scatter(x=st.session_state.company.dfCompany.index,y=st.session_state.company.dfCompany['Close'].rolling(window=20).mean(),marker_color='blue',name='20 Day MA'))
                chtInd20MA.add_trace(go.Bar(x=st.session_state.company.dfCompany.index, y=st.session_state.company.dfCompany['Volume'], name='Volume', marker={'color':'orange'}), secondary_y=True)
                chtInd20MA.update_yaxes(range=[0,70000000],secondary_y=True)
                chtInd20MA.update_yaxes(visible=False, secondary_y=True)
                chtInd20MA.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
                chtInd20MA.update_layout(title={'text':f'{st.session_state.selTicker}', 'x':0.5})
                chtInd20MA.show()                
                st.plotly_chart(chtInd20MA, use_container_width=True)
        except Exception as ex:    
            st.write(f"Exception {ex}")               
    with tabIndicator60:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                chtInd20MA = make_subplots(specs=[[{"secondary_y": True}]])
                chtInd20MA.add_trace(go.Candlestick(x=st.session_state.company.dfCompany.index,
                                            open=st.session_state.company.dfCompany['Open'],
                                            high=st.session_state.company.dfCompany['High'],
                                            low=st.session_state.company.dfCompany['Low'],
                                            close=st.session_state.company.dfCompany['Close'],
                                            name='Price'))
                chtInd20MA.add_trace(go.Scatter(x=st.session_state.company.dfCompany.index,y=st.session_state.company.dfCompany['Close'].rolling(window=60).mean(),marker_color='blue',name='60 Day MA'))
                chtInd20MA.add_trace(go.Bar(x=st.session_state.company.dfCompany.index, y=st.session_state.company.dfCompany['Volume'], name='Volume', marker={'color':'orange'}), secondary_y=True)
                chtInd20MA.update_yaxes(range=[0,70000000],secondary_y=True)
                chtInd20MA.update_yaxes(visible=False, secondary_y=True)
                chtInd20MA.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
                chtInd20MA.update_layout(title={'text':f'{st.session_state.selTicker}', 'x':0.5})
                chtInd20MA.show()                
                st.plotly_chart(chtInd20MA, use_container_width=True)
        except Exception as ex:    
            st.write(f"Exception {ex}")               
    with tabIndicator180:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                chtInd20MA = make_subplots(specs=[[{"secondary_y": True}]])
                chtInd20MA.add_trace(go.Candlestick(x=st.session_state.company.dfCompany.index,
                                            open=st.session_state.company.dfCompany['Open'],
                                            high=st.session_state.company.dfCompany['High'],
                                            low=st.session_state.company.dfCompany['Low'],
                                            close=st.session_state.company.dfCompany['Close'],
                                            name='Price'))
                chtInd20MA.add_trace(go.Scatter(x=st.session_state.company.dfCompany.index,y=st.session_state.company.dfCompany['Close'].rolling(window=180).mean(),marker_color='blue',name='180 Day MA'))
                chtInd20MA.add_trace(go.Bar(x=st.session_state.company.dfCompany.index, y=st.session_state.company.dfCompany['Volume'], name='Volume', marker={'color':'orange'}), secondary_y=True)
                chtInd20MA.update_yaxes(range=[0,70000000],secondary_y=True)
                chtInd20MA.update_yaxes(visible=False, secondary_y=True)
                chtInd20MA.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
                chtInd20MA.update_layout(title={'text':f'{st.session_state.selTicker}', 'x':0.5})
                chtInd20MA.show()                
                st.plotly_chart(chtInd20MA, use_container_width=True)
        except Exception as ex:    
            st.write(f"Exception {ex}")               
    with tabIndicator360:
        try:
            if(st.session_state.selTicker is not None and len(st.session_state.selTicker)>0):
                chtInd20MA = make_subplots(specs=[[{"secondary_y": True}]])
                chtInd20MA.add_trace(go.Candlestick(x=st.session_state.company.dfCompany.index,
                                            open=st.session_state.company.dfCompany['Open'],
                                            high=st.session_state.company.dfCompany['High'],
                                            low=st.session_state.company.dfCompany['Low'],
                                            close=st.session_state.company.dfCompany['Close'],
                                            name='Price'))
                chtInd20MA.add_trace(go.Scatter(x=st.session_state.company.dfCompany.index,y=st.session_state.company.dfCompany['Close'].rolling(window=360).mean(),marker_color='blue',name='360 Day MA'))
                chtInd20MA.add_trace(go.Bar(x=st.session_state.company.dfCompany.index, y=st.session_state.company.dfCompany['Volume'], name='Volume', marker={'color':'orange'}), secondary_y=True)
                chtInd20MA.update_yaxes(range=[0,70000000],secondary_y=True)
                chtInd20MA.update_yaxes(visible=False, secondary_y=True)
                chtInd20MA.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
                chtInd20MA.update_layout(title={'text':f'{st.session_state.selTicker}', 'x':0.5})
                chtInd20MA.show()                
                st.plotly_chart(chtInd20MA, use_container_width=True)
        except Exception as ex:    
            st.write(f"Exception {ex}")               


init()