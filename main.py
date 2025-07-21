import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💸 Dashboard Spese Personali")

# ✅ Usa pandas per leggere il CSV
df = pd.read_csv("spese.csv")

# 📊 Mostra i dati
st.write("📊 Spese registrate:")
st.dataframe(df)

# 💰 Calcolo del totale
totale = df["importo"].sum()
st.metric("Totale spese", f"{totale:.2f} €")

# 🥧 Grafico a torta
fig = px.pie(df, values="importo", names="categoria", title="Distribuzione per categoria")
st.plotly_chart(fig)
