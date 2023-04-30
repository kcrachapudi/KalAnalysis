import streamlit as st
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def GetAggrid(dfData):
    gb = GridOptionsBuilder.from_dataframe(dfData)
    #gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True) 
    gridOptions = gb.build()

    grid_response = AgGrid(
        dfData,
        gridOptions=gridOptions,
        fit_columns_on_grid_load=True,
        theme='alpine', #Add theme color to the table
        enable_enterprise_modules=True,
        height=350, 
        width='100%',
        reload_data=True
    )
    return grid_response