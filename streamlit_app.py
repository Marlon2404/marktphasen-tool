import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 🎯 Streamlit App Titel
st.title("🚀 Marktphasen-Tool")
st.subheader("📈 Bitcoin Live-Chart mit Marktanalyse")

# 📅 Nutzer kann Startdatum auswählen
start_date = st.date_input("📆 Wähle das Startdatum:", value=pd.to_datetime("2017-01-01"))

# ✅ BTC-Daten abrufen (sicherstellen, dass sie richtig geladen werden)
@st.cache_data
def load_data(start_date):
    btc = yf.download("BTC-USD", start=start_date.strftime("%Y-%m-%d"), interval="1d", progress=False)

    # **Fix für das falsche Datumsformat**
    btc = btc.reset_index()  
    btc["Date"] = pd.to_datetime(btc["Date"])  # Sicherstellen, dass Datum korrekt ist
    return btc

btc = load_data(start_date)

# 🛠️ **DEBUG-SCHRITT: Zeige die geladenen BTC-Daten als Tabelle**
st.write("📊 **Debug: BTC-Daten**")
st.write(btc.head())  # Zeigt die ersten Zeilen der Daten

# 🔁 Falls keine Daten geladen wurden, Fehler anzeigen
if btc.empty:
    st.error("❌ Fehler: Konnte keine BTC-Daten abrufen. Bitte probiere ein anderes Datum.")
    st.stop()

# 🎨 **TradingView-ähnliches BTC-Chart mit Plotly**
fig = go.Figure()

# 🔶 BTC-Preis als Linie
fig.add_trace(go.Scatter(
    x=btc["Date"],  # **Fix: Sicherstellen, dass das Datum korrekt verarbeitet wird**
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
    xaxis=dict(type="date"),  # **Fix für die falsche Zeitachse**
    template="plotly_dark",
    height=600
)

# 🔹 **Chart anzeigen**
st.plotly_chart(fig)
