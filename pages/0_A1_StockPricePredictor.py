import streamlit as st  # Streamlit for web interface
import yfinance as yf  # To fetch historical stock data
import pandas as pd  # Data manipulation
import numpy as np  # Numerical operations
import datetime  # Date handling
from sklearn.preprocessing import MinMaxScaler  # Normalize input features
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  # Evaluation metrics
from tensorflow.keras.models import Model, load_model  # Keras Model API
from tensorflow.keras.layers import Input, LSTM, Bidirectional, Dense, Dropout, Attention, Concatenate  # Model layers
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.callbacks import EarlyStopping  # Early stopping to prevent overfitting
from sklearn.model_selection import train_test_split  # For splitting data into train/test sets
import plotly.graph_objs as go  # Interactive plotting
import io  # For CSV download
import os  # For checking model existence
from pathlib import Path  # For file path handling

# Sidebar inputs for user interaction
st.sidebar.title("Stock Prediction Settings")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")  # Default to AAPL
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))  # Default start date
end_date = st.sidebar.date_input("End Date", datetime.date.today())  # Default end date
future_days = st.sidebar.slider("Days to Forecast", min_value=1, max_value=30, value=5)
epochs = st.sidebar.slider("Training Epochs", min_value=5, max_value=100, value=10, step=5)
batch_size = st.sidebar.slider("Batch Size", min_value=16, max_value=128, value=32, step=16)
save_model_option = st.sidebar.checkbox("Save Trained Model", value=True)
load_model_option = st.sidebar.checkbox("Load Existing Model if Available", value=True)
run_button = st.sidebar.button("Run Prediction")

abspath =  Path(__file__).parent.parent.absolute()

if run_button:
    # Clear cache and session state to avoid stale data
    st.session_state.run_button = True
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.clear()        

    data_folder = "TickerData"
    model_folder = "SavedMLModels"

    data_path = abspath.joinpath(data_folder, f"{ticker}_data.csv")
    model_path = abspath.joinpath(model_folder, "A1_StockPricePredictor_model.h5")

    today_str = datetime.date.today().isoformat()
    data = pd.DataFrame()
    if os.path.exists(data_path):
        mod_time = datetime.date.fromtimestamp(os.path.getmtime(data_path)).isoformat()
        if mod_time == today_str:
            data = pd.read_csv(data_path, index_col=0, parse_dates=True)
        else:
            # Download historical stock data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date, multi_level_index=False)
            data.to_csv(data_path)
    else:
        # Download historical stock data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date, multi_level_index=False)
        data.to_csv(data_path)

    #Data Preview 
    st.subheader(f"{ticker} Historical Data")
    st.write(data.head())  # Display the first few rows of the data
    st.write(data.tail())  # Display the last few rows of the data

    # --- Technical Indicator Calculations ---
    def calculate_rsi(series, period=14):
        rsi = series.copy()
        try:
            # Calculate the RSI using the standard formula
            delta = series.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        except Exception as e:
            st.error(f"Error calculating RSI: {e}")
            rsi = pd.Series([np.nan] * len(series))    
        return rsi

    def calculate_macd(series, short=12, long=26, signal=9):
        short_ema = series.ewm(span=short, adjust=False).mean()
        long_ema = series.ewm(span=long, adjust=False).mean()
        macd = short_ema - long_ema
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    def calculate_bollinger_bands(series, window=20):
        sma = series.rolling(window).mean()
        std = series.rolling(window).std()
        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)
        return upper_band, lower_band

    def calculate_obv(df:pd.DataFrame) -> pd.DataFrame:
        obv = [0]  # Initialize with 0 for the first OBV value
        for i in range(1, len(df)):
            if df['Close'].iloc[i] > df['Close'].iloc[i - 1]:
                obv.append(obv[-1] + df['Volume'].iloc[i])
            elif df['Close'].iloc[i] < df['Close'].iloc[i - 1]:
                obv.append(obv[-1] - df['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        df['OBV'] = obv
        return df

    def calculate_stochastic_oscillator(high, low, close, k_window=14, d_window=3):
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d = k.rolling(window=d_window).mean()
        return k, d

    # Add indicators to dataframe
    data['RSI'] = calculate_rsi(data['Close'])
    data['MACD'], data['Signal'] = calculate_macd(data['Close'])
    data['BB_High'], data['BB_Low'] = calculate_bollinger_bands(data['Close'])
    data = calculate_obv(data)
    data['Stoch_K'], data['Stoch_D'] = calculate_stochastic_oscillator(data['High'], data['Low'], data['Close'])
    st.subheader(f"{ticker} Data with Technical Indicators")
    st.write(data.head())  # Display the first few rows of the data
    st.write(data.tail())  # Display the last few rows of the data
    data = data.dropna()

    # Feature engineering
    features = ['Close', 'RSI', 'MACD', 'Signal', 'BB_High', 'BB_Low', 'OBV', 'Stoch_K', 'Stoch_D']
    if data.empty or len(data) < 2:
        st.error("Not enough data after computing indicators. Try selecting a longer date range.")
        st.stop()
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data[features])

    # Create sequences
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i - seq_length:i])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    SEQ_LEN = 60
    X, y = create_sequences(scaled_data, SEQ_LEN)

    # Define model
    def build_model(input_shape):
        inputs = Input(shape=input_shape)
        x = Bidirectional(LSTM(64, return_sequences=True))(inputs)
        x = Dropout(0.2)(x)
        attention = Attention()([x, x])
        x = Concatenate()([x, attention])
        x = LSTM(64)(x)
        x = Dropout(0.2)(x)
        outputs = Dense(1)(x)
        model = Model(inputs, outputs)
        model.compile(optimizer='adam', loss=MeanSquaredError())
        return model

    # Train model
    if os.path.exists(model_path):
        model = load_model(model_path, compile=False)
        model.compile(optimizer='adam', loss=MeanSquaredError())
        st.success("Loaded existing model.")
    else:
        model = build_model((X.shape[1], X.shape[2]))
        with st.spinner("Training model..."):
            model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
            model.save(model_path)

    # Predict
    preds = model.predict(X)
    actual = scaler.inverse_transform(np.concatenate([y.reshape(-1, 1), np.zeros((y.shape[0], scaled_data.shape[1]-1))], axis=1))[:, 0]
    preds_inverse = scaler.inverse_transform(np.concatenate([preds, np.zeros((preds.shape[0], scaled_data.shape[1]-1))], axis=1))[:, 0]

    # Metrics
    rmse = np.sqrt(mean_squared_error(actual, preds_inverse))
    mae = mean_absolute_error(actual, preds_inverse)
    r2 = r2_score(actual, preds_inverse)
    st.metric("RMSE", f"{rmse:.2f}")
    st.metric("MAE", f"{mae:.2f}")
    st.metric("R² Score", f"{r2:.2f}")

    # Plot actual vs predicted
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index[-len(actual):], y=actual, name='Actual', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index[-len(preds_inverse):], y=preds_inverse, name='Predicted', line=dict(color='orange')))
    fig.update_layout(title=f"{ticker} Stock Price Prediction", xaxis_title="Date", yaxis_title="Price", legend=dict(x=0, y=1))
    st.plotly_chart(fig, use_container_width=True)

    # Create and Download actual vs predicted 
    comparison_df = pd.DataFrame({
        "Date": data.index[-len(actual):],
        "Actual Close": actual,
        "Predicted Close": preds_inverse
    })
    comparison_df.set_index("Date", inplace=True)
    st.subheader("Actual vs Predicted Values")
    st.dataframe(comparison_df)
    # Download option
    csv_actual_vs_pred = comparison_df.to_csv().encode("utf-8")
    st.download_button("Download Actual vs Predicted CSV", csv_actual_vs_pred, "actual_vs_predicted.csv", "text/csv")


    # Future Forecasting
    last_seq = scaled_data[-SEQ_LEN:]
    future_preds = []
    for _ in range(future_days):
        input_seq = last_seq.reshape(1, SEQ_LEN, scaled_data.shape[1])
        next_pred = model.predict(input_seq)[0][0]
        future_preds.append(next_pred)
        next_seq = np.append(last_seq[1:], [[next_pred] + list(last_seq[-1, 1:])], axis=0)
        last_seq = next_seq

    # Inverse transform future predictions
    future_dates = pd.date_range(data.index[-1] + pd.Timedelta(days=1), periods=future_days, freq='B')
    future_inverse = scaler.inverse_transform(np.concatenate([np.array(future_preds).reshape(-1, 1), np.zeros((future_days, scaled_data.shape[1]-1))], axis=1))[:, 0]

    # Plot future predictions
    future_fig = go.Figure()
    future_fig.add_trace(go.Scatter(x=future_dates, y=future_inverse, name='Future Forecast', line=dict(color='green')))
    future_fig.update_layout(title="Future Forecast", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(future_fig, use_container_width=True)

    # Download CSV
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted Close": future_inverse})
    csv = forecast_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Forecast CSV", csv, "forecast.csv", "text/csv")

    # Completion
    st.success("Model training, evaluation, and forecasting complete.")
    st.balloons()
