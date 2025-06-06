import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Snapshot", layout="centered")

st.title("📈 Stock Info Snapshot")

# Sidebar input
ticker_input = st.text_input("Enter a stock ticker symbol", value="AAPL")

if ticker_input:
    try:
        ticker = yf.Ticker(ticker_input.upper())
        info = ticker.info
        hist = ticker.history(period="5d", interval="1d")

        # Location
        location = f"{info.get('city', 'Unknown')}, {info.get('state', '')} {info.get('country', '')}".strip(", ")

        # Options available
        has_options = len(ticker.options) > 0

        # Volume stats
        avg_volume = info.get("averageVolume", None)
        current_volume = hist["Volume"][-1] if not hist.empty else None
        rvol = round(current_volume / avg_volume, 2) if avg_volume and current_volume else "N/A"

        # Last earnings
        earnings = info.get("earningsDate", None)
        if isinstance(earnings, list) and earnings:
            last_earnings = earnings[0].strftime('%Y-%m-%d')
        elif isinstance(earnings, datetime):
            last_earnings = earnings.strftime('%Y-%m-%d')
        else:
            last_earnings = "N/A"

        # PE ratio
        pe_ratio = info.get("trailingPE", "N/A")

        # Display results
        st.subheader(f"Results for {ticker_input.upper()}")

        st.markdown(f"**📍 Company Location:** {location}")
        st.markdown(f"**📝 Options Available:** {'Yes' if has_options else 'No'}")
        st.markdown(f"**📊 Average Volume:** {avg_volume:,}" if avg_volume else "N/A")
        st.markdown(f"**📈 Relative Volume (RVOL):** {rvol}")
        st.markdown(f"**🗓️ Last Earnings Date:** {last_earnings}")
        st.markdown(f"**💰 P/E Ratio:** {pe_ratio}")

    except Exception as e:
        st.error(f"Error retrieving data for ticker '{ticker_input.upper()}': {e}")
