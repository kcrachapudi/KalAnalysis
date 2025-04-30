# app.py

import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Market Grid Dashboard", layout="wide")
st.title("📊 Market Dashboard (Grid View)")

symbols = {
    "Dow Jones (DJI)": "^DJI",
    "Nasdaq QQQ": "QQQ",
    "S&P 500 (SPY)": "SPY",
    "WTI Crude Oil": "CL=F",
    "10Y Treasury Yield": "^TNX",
    "Volatility Index (VIX)": "^VIX"
}

@st.cache_data(ttl=900)
def get_data(symbol):
    return yf.download(symbol, period="2d", interval="1d", multi_level_index=False)

# Create 3-column layout
cols = st.columns(3)

for i, (name, symbol) in enumerate(symbols.items()):
    data = get_data(symbol)
    if len(data) < 2:
        cols[i % 3].warning(f"Data unavailable for {name}")
        continue

    prev_close = data['Close'].iloc[-2]
    latest_close = data['Close'].iloc[-1]
    change_pct = (latest_close - prev_close) / prev_close * 100

    color = "green" if change_pct >= 0 else "red"
    sign = "+" if change_pct >= 0 else ""

    with cols[i % 3]:
        st.markdown(f"""
        <div style='font-size:18px; padding:15px; border-radius:10px; 
                    background-color:#f0f2f6; border-left: 5px solid {color}; margin-bottom:15px'>
            <b>{name}</b><br>
            <span style='color:{color}; font-size:22px'>
                {latest_close:.2f} ({sign}{change_pct:.2f}%)
            </span>
        </div>
        """, unsafe_allow_html=True)
