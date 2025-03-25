import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 🎯 Streamlit App Titel
st.title("🚀 Marktphasen-Tool")
st.subheader("📈 Bitcoin Live-Chart mit Marktanalyse")

# 📅 Nutzer kann Startdatum auswählen
start_date = st.date_input("📆 Wähle das Startdatum:", value=pd.to_datetime("2017-01-01"))
end_date = pd.to_datetime("today")  # **Setzt das Enddatum auf heute!**

# ✅ BTC-Daten abrufen (Korrekte Periode sichern)
@st.cache_data
def load_data(start_date, end_date):
    btc = yf.download("BTC-USD", start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), interval="1d", progress=False)

    # **Fix für das falsche Datumsformat**
    btc.reset_index(inplace=True)  
    btc["Date"] = pd.to_datetime(btc["Date"])  # Sicherstellen, dass Datum korrekt ist
    return btc

btc = load_data(start_date, end_date)

# 🛠️ **DEBUG-SCHRITT: Zeige die ersten 10 Datenzeilen**
st.write("📊 **Debug: BTC-Daten (erste 10 Zeilen)**")
st.write(btc.head(10))  

# 🔁 Falls keine Daten geladen wurden, Fehler anzeigen
if btc.empty:
    st.error("❌ Fehler: Konnte keine BTC-Daten abrufen. Bitte probiere ein anderes Datum.")
    st.stop()

# 🎨 **BTC-Preislinie korrekt plotten**
fig = go.Figure()

# 🔶 BTC-Preis als Linie mit richtiger Zeitachse!
fig.add_trace(go.Scatter(
    x=btc["Date"],  # **Fix: Nutze korrekt formatiertes Datum**
    y=btc["Close"],
    mode='lines',
    name='BTC/USD',
    line=dict(color='orange')
))

# 🛠️ **Fix: Sicherstellen, dass X-Achse korrekt skaliert wird**
fig.update_xaxes(type="date")

# 📊 **Layout anpassen**
fig.update_layout(
    title="Bitcoin Kursverlauf (BTC/USD)",
    xaxis_title="Datum",
    yaxis_title="Preis in USD",
    template="plotly_dark",
    height=600
)

# 🔹 **Chart anzeigen (mit mehr Debugging)**
st.write("📊 **Debug: Plotly Chart-JSON**")
st.write(fig.to_json())  # **DEBUG: Zeigt, ob das Chart korrekt generiert wird!**

st.plotly_chart(fig)

