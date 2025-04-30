# app.py

import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Market Grid Dashboard", layout="wide")
st.title("📊 Market Dashboard")

symbols = {
    "Dow Jones (DJI)": "^DJI",
    "Nasdaq QQQ": "QQQ",
    "S&P 500 (SPY)": "SPY",

    "10Y Treasury Yield": "^TNX",
    "2Y Treasury Yield": "^IRX",
    "Dollar Index": "DX-Y.NYB",

    "WTI Crude Oil": "WTI",
    "Natural Gas": "NG=F",
    "Volatility Index (VIX)": "^VIX",

    "Gold Index": "GC=F",
    "Silver Index": "SI=F",
    "Copper Index": "HG=F",

    "Corn Index": "ZC=F",
    "Soybean Index": "ZS=F",
    "Wheat Index": "ZW=F",

    "Bitcoin": "BTC-USD",
    "Solana": "SOL-USD",
    "Ethereum": "ETH-USD"
}

@st.cache_data(ttl=900)
def get_data(symbol):
    return yf.download(symbol, period="14d", interval="1d", multi_level_index=False)  # More days to detect streaks

def get_streak_info(close_prices):
    direction = None
    count = 0
    total_pct = 0.0

    for i in range(len(close_prices) - 1, 0, -1):
        today = close_prices[i]
        yesterday = close_prices[i - 1]
        pct_change = (today - yesterday) / yesterday * 100

        if pct_change == 0:
            break  # Flat day, end streak

        current_dir = "up" if pct_change > 0 else "down"

        if direction is None:
            direction = current_dir

        if current_dir == direction:
            count += 1
            total_pct += pct_change
        else:
            break

    return direction, count, total_pct

# Grid layout
cols = st.columns(3)

for i, (name, symbol) in enumerate(symbols.items()):
    df = get_data(symbol)
    df.dropna(inplace=True)

    if len(df) < 2:
        cols[i % 3].warning(f"Not enough data for {name}")
        continue

    prev_close = df['Close'].iloc[-2]
    latest_close = df['Close'].iloc[-1]
    change_pct = (latest_close - prev_close) / prev_close * 100

    direction = "up" if change_pct >= 0 else "down"
    color = "green" if direction == "up" else "red"
    sign = "+" if change_pct >= 0 else ""

    # Get streak info
    streak_dir, streak_count, streak_pct = get_streak_info(df['Close'].values)
    arrow = "↑" if streak_dir == "up" else "↓"
    streak_color = "green" if streak_dir == "up" else "red"
    streak_sign = "+" if streak_pct >= 0 else ""

    with cols[i % 3]:
        st.markdown(f"""
        <div style='font-size:18px; padding:15px; border-radius:10px; 
                    background-color:#f0f2f6; border-left: 5px solid {color}; margin-bottom:15px'>
            <b>{name}</b><br>
            <span style='color:{color}; font-size:22px'>
                {latest_close:.2f} ({sign}{change_pct:.2f}%)
            </span><br>
            <span style='color:{streak_color}; font-size:16px'>
                {arrow} {streak_count} session{'s' if streak_count > 1 else ''} ({streak_sign}{streak_pct:.2f}%)
            </span>
        </div>
        """, unsafe_allow_html=True)
