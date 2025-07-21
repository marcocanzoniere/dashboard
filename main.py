import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def init_db():
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS spese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            descrizione TEXT,
            importo REAL
        )
    """)
    conn.commit()
    conn.close()

def aggiungi_spesa(categoria, descrizione, importo):
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("INSERT INTO spese (categoria, descrizione, importo) VALUES (?, ?, ?)", (categoria, descrizione, importo))
    conn.commit()
    conn.close()

def leggi_spese():
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("SELECT categoria, descrizione, importo FROM spese")
    dati = c.fetchall()
    conn.close()
    df = pd.DataFrame(dati, columns=["categoria", "descrizione", "importo"])
    return df

st.title("💸 Dashboard Spese Personali")

init_db()  # Inizializza database e tabella

with st.form("inserisci_spesa"):
    categoria = st.selectbox("Categoria", ["Cibo", "Affitto", "Trasporti", "Svago", "Altro"])
    descrizione = st.text_input("Descrizione")
    importo = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Aggiungi spesa")

    if submitted:
        aggiungi_spesa(categoria, descrizione, importo)
        st.success("Spesa aggiunta!")

# Leggiamo le spese salvate dal database
df = leggi_spese()

st.write("📊 Spese registrate:")
st.dataframe(df)

totale = df["importo"].sum() if not df.empty else 0
st.metric("Totale spese", f"{totale:.2f} €")

if not df.empty:
    fig = px.pie(df, values="importo", names="categoria", title="Distribuzione per categoria")
    st.plotly_chart(fig)
else:
    st.info("Inserisci spese per visualizzare il grafico.")
