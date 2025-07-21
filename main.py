import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import hashlib

def init_db():
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS spese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            categoria TEXT,
            descrizione TEXT,
            importo REAL,
            FOREIGN KEY(user_id) REFERENCES utenti(id)
        )
    """)
    conn.commit()
    conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def registra_utente(username, password):
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def autentica(username, password):
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("SELECT id, password FROM utenti WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and hash_password(password) == row[1]:
        return row[0]  # ritorna user_id
    return None

def aggiungi_spesa(user_id, categoria, descrizione, importo):
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("INSERT INTO spese (user_id, categoria, descrizione, importo) VALUES (?, ?, ?, ?)",
              (user_id, categoria, descrizione, importo))
    conn.commit()
    conn.close()

def leggi_spese(user_id):
    conn = sqlite3.connect("spese.db")
    c = conn.cursor()
    c.execute("SELECT categoria, descrizione, importo FROM spese WHERE user_id = ?", (user_id,))
    dati = c.fetchall()
    conn.close()
    return pd.DataFrame(dati, columns=["categoria", "descrizione", "importo"])

# --- Streamlit App ---

st.title("💸 Dashboard Spese Personali Multi-Utente")

init_db()

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    pagina = st.sidebar.selectbox("Vai a", ["Login", "Registrati"])

    if pagina == "Registrati":
        st.header("Registrazione")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Registrati"):
            if registra_utente(username, password):
                st.success("Utente registrato! Ora fai login.")
            else:
                st.error("Username già esistente.")

    else:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id = autentica(username, password)
            if user_id:
                st.session_state.user_id = user_id
                #st.experimental_rerun()
            else:
                st.error("Username o password errati.")
else:
    st.sidebar.write(f"Sei loggato con user id: {st.session_state.user_id}")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        #st.experimental_rerun()

    with st.form("inserisci_spesa"):
        categoria = st.selectbox("Categoria", ["Cibo", "Affitto", "Trasporti", "Svago", "Altro"])
        descrizione = st.text_input("Descrizione")
        importo = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Aggiungi spesa")

        if submitted:
            aggiungi_spesa(st.session_state.user_id, categoria, descrizione, importo)
            st.success("Spesa aggiunta!")

    df = leggi_spese(st.session_state.user_id)

    st.write("📊 Le tue spese:")
    st.dataframe(df)

    totale = df["importo"].sum() if not df.empty else 0
    st.metric("Totale spese", f"{totale:.2f} €")

    if not df.empty:
        fig = px.pie(df, values="importo", names="categoria", title="Distribuzione per categoria")
        st.plotly_chart(fig)
    else:
        st.info("Inserisci spese per visualizzare il grafico.")
