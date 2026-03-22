import streamlit as st
import requests
import pandas as pd

st.title("₿ Crypto Dashboard ₿")


coin = st.sidebar.selectbox("Select Coin", ["bitcoin", "ethereum", "dogecoin"])
days = st.sidebar.selectbox("Select Days", [1, 7, 14, 30])
@st.cache_data(ttl=300)
def get_price_data(coin, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}


    try:
        response = requests.get(url, params=params, timeout=10)
    except:
        st.error("Network error")
        return None

    if response.status_code != 200:
        st.error(f"API failed (status {response.status_code})")
        return None
    
    data = response.json()
    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df


df = get_price_data(coin, days)

if df is not None:

    st.subheader(f"{coin.capitalize()} Price ({days} days)")

    current_price = df["price"].iloc[-1]
    old_price = df["price"].iloc[0]
    change = current_price - old_price
    percent_change = (change / old_price) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{change:+.2f} ({percent_change:+.2f}%)"
        )

    st.markdown("---")

    st.line_chart(df.set_index("timestamp")["price"])

    
    
    st.markdown("---")

    st.dataframe(df)