import streamlit as st

CURRENT_THEME = "blue"
IS_DARK_THEME = True

def run():
    st.set_page_config(page_title = "KalAnalysis Fun Stock and Crypto Analysis", layout="wide")
    body()
    sidebar()

def body():
    st.write(
    """
    # KalAnalysis.com
    Fun AI based Quant Stock and Crypto Analysis to analyze trends and predict outcomes.
    """
    )

def sidebar():
    st.sidebar.write("Fun and educative Stock and Crypto Analysis")

run()