import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Stock Analysis Dashboard")

# Sidebar input
with st.sidebar:
    st.header("Stock Selection")
    ticker = st.text_input("Enter Stock Ticker", value="AAPL")
    run_button = st.button("Get Stock Data")

# Format helper
def format_number(value):
    try:
        if isinstance(value, (int, float)):
            return f"{value:,.2f}"
    except Exception as e:
        return ""
    return str(value)

# Metric info
metric_info = {
    "Open": {"Alt":"open", "desc": "Opening price.", "high_is_good": True},
    "High": {"Alt":"dayHigh", "desc": "Highest price.", "high_is_good": True},
    "Low":  {"Alt":"dayLow", "desc": "Lowest price.", "high_is_good": False},
    "Close": {"Alt":"previousClose", "desc": "Closing price.", "high_is_good": True},
    "Volume": {"Alt":"volume", "desc": "Trading volume.", "high_is_good": True},
    "Market Cap": {"Alt":"marketCap", "desc": "Total company value (shares × price).", "high_is_good": True},
    "Enterprise Value": {"Alt":"enterpriseValue", "desc": "Market cap + debt - cash.", "high_is_good": True},
    "Trailing P/E": {"Alt":"trailingPE", "desc": "Price-to-earnings ratio (past 12 months).", "high_is_good": False, "ideal": 15},
    "Forward P/E": {"Alt":"forwardPE", "desc": "Price-to-earnings ratio (forecast).", "high_is_good": False, "ideal": 15},
    "EPS (TTM)": {"Alt":"trailingEps", "desc": "Earnings per share (trailing 12 months).", "high_is_good": True},
    "EPS (Forward)": {"Alt":"forwardEps", "desc": "Projected earnings per share.", "high_is_good": True},
    "Profit Margin": {"Alt":"profitMargins", "desc": "Net income as % of revenue.", "high_is_good": True},
    "Operating Margin": {"Alt":"operatingMargins", "desc": "Operating income as % of revenue.", "high_is_good": True},
    "Return on Assets": {"Alt":"returnOnAssets", "desc": "Net income ÷ assets.", "high_is_good": True},
    "Return on Equity": {"Alt":"returnOnEquity", "desc": "Net income ÷ equity.", "high_is_good": True},
    "Revenue (TTM)": {"Alt":"totalRevenue", "desc": "Revenue in the last 12 months.", "high_is_good": True},
    "Gross Profits": {"Alt":"grossProfits", "desc": "Revenue minus COGS.", "high_is_good": True},
    "EBITDA": {"Alt":"ebitda", "desc": "Earnings before interest, taxes, depreciation, and amortization."},
    "Shares Outstanding": {"Alt":"sharesOutstanding", "desc": "Total shares issued."},
    "Float": {"Alt":"floatShares", "desc": "Publicly available shares."},
    "Debt to Equity": {"Alt":"debtToEquity", "desc": "Debt relative to equity. Lower is better.", "high_is_good": False, "ideal": 1},
    "Current Ratio": {"Alt":"currentRatio", "desc": "Assets ÷ liabilities. >1 is good.", "ideal": 1.5},
    "Quick Ratio": {"Alt":"quickRatio", "desc": "Quick assets ÷ liabilities.", "ideal": 1},
    "Beta": {"Alt":"beta", "desc": "Volatility vs market. <1 = stable.", "ideal": 1},
    "52 Week High": {"Alt":"fiftyTwoWeekHigh", "desc": "Yearly highest price."},
    "52 Week Low": {"Alt":"fiftyTwoWeekLow", "desc": "Yearly lowest price."},
    "50 Day MA": {"Alt":"fiftyDayAverage", "desc": "50-day moving average."},
    "200 Day MA": {"Alt":"twoHundredDayAverage", "desc": "200-day moving average."},
    "Shares Short": {"Alt":"sharesShort", "desc": "Shares shorted."},
    "Short Ratio": {"Alt":"shortRatio", "desc": "Ratio of shorted shares."},
    "Short % of Float": {"Alt":"shortPercentOfFloat", "desc": "Shares shorted relative to float."},
}

# Color logic
def get_color(value, meta):
    try:
        if not isinstance(value, (int, float)):
            return "#444"
        ideal = meta.get("ideal")
        if "high_is_good" in meta:
            if meta["high_is_good"]:
                return "green" if value >= ideal else "red" if ideal else "#444"
            else:
                return "red" if ideal and value > ideal else "green"
        elif ideal is not None:
            return "green" if abs(value - ideal) < ideal * 0.5 else "red"
    except Exception as e:
        return "#444"
    return "#444"

# Metric fetcher from get_info/fast_info
def get_metric_value(key, info_dict):
    key_variants = [
        key,
        key.replace(" ", "").lower(),
        key.replace(" ", "_").lower(),
        key.lower(),
    ]
    for k in key_variants:
        if k in info_dict:
            return info_dict[k]
        elif k in metric_info:
            alt_key = metric_info[k].get("Alt", "")
            if alt_key in info_dict:
                return info_dict[alt_key]
    return None

# Main app logic
if run_button and ticker:
    try:
        stock = yf.Ticker(ticker)
        spy_trailingPE = None
        nasdaq_trailingPE = None
        # Fetch SPY and NASDAQ trailing P/E ratios
        try:
            spy = yf.Ticker("SPY")
            spy_info = spy.get_info()
            spy_trailingPE = spy_info.get("trailingPE")
        except Exception as e:
            st.warning(f"Could not fetch SPY data: {e}")
            spy_trailingPE = None
        try:
            info = stock.get_info()
        except Exception as e:
            st.warning(f"Could not fetch detailed info: {e}")
            info = {}
        st.subheader(f"🔍 Key Metrics for {ticker.upper()}")

        # Extract available metrics
        metric_items = []
        for label, meta in metric_info.items():
            value = get_metric_value(label, info)
            metric_items.append((label, value))

        metric_items.append(("SPY Trailing P/E", spy_trailingPE))

        # Render in 4-column grid
        for i in range(0, len(metric_items), 4):
            cols = st.columns(4)
            for col, (label, value_raw) in zip(cols, metric_items[i:i+4]):
                meta = metric_info.get(label, {})
                tooltip = meta.get("desc", "")
                color = get_color(value_raw, meta)
                val = format_number(value_raw)
                col.markdown(f"""
                    <div title="{tooltip}" style="background-color: #f9f9f9; padding: 10px;
                        border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 17px; color: #666;">{label}</div>
                        <div style="font-size: 15px; font-weight: 600; color: {color};">{val}</div>
                    </div>
                """, unsafe_allow_html=True)

        fin_data = stock.financials.T
        eps_data = stock.earnings_history

        # Color Legend
        st.markdown("""
        <br>
        <div style="display: flex; gap: 20px; align-items: center;">
            <div style="background-color: green; width: 16px; height: 16px; border-radius: 3px;"></div>
            <span style="font-size: 14px;">Good / Healthy</span>
            <div style="background-color: red; width: 16px; height: 16px; border-radius: 3px;"></div>
            <span style="font-size: 14px;">Needs Attention / Poor</span>
            <div style="background-color: #444; width: 16px; height: 16px; border-radius: 3px;"></div>
            <span style="font-size: 14px;">Neutral / No Target</span>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")