import streamlit as st
import yfinance as yf
import pandas as pd  # ✅ Hier Pandas importieren!
import plotly.graph_objects as go

# 🎯 Streamlit App Titel
st.title("🚀 Marktphasen-Tool")
st.subheader("📈 Bitcoin Live-Chart mit Marktanalyse")

# 📅 Nutzer kann Startdatum auswählen
start_date = st.date_input("📆 Wähle das Startdatum:", value=pd.to_datetime("2017-01-01"))

# ✅ BTC-Daten von Yahoo Finance abrufen
@st.cache_data
def load_data():
    btc = yf.download("BTC-USD", start=start_date.strftime("%Y-%m-%d"), interval="1d", progress=False)
    return btc

btc = load_data()

# 🔁 Sicherheits-Check: Falls keine Daten geladen wurden
if btc.empty:
    st.error("❌ Fehler: Konnte keine BTC-Daten abrufen. Bitte probiere ein anderes Datum.")
    st.stop()

# 🎨 TradingView-ähnliches BTC-Chart mit Plotly
fig = go.Figure()

# 🔶 BTC-Preis als Linie
fig.add_trace(go.Scatter(
    x=btc.index,
    y=btc["Close"],
    mode='lines',
    name='BTC/USD',
    line=dict(color='orange')
))

# 📊 Chart-Layout optimieren
fig.update_layout(
    title="Bitcoin Kursverlauf (BTC/USD)",
    xaxis_title="Datum",
    yaxis_title="Preis in USD",
    template="plotly_dark",
    height=600
)

# 🔹 Chart anzeigen
st.plotly_chart(fig)

