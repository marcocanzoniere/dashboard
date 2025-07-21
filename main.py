import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💸 Dashboard Spese Personali")

# Lista o DataFrame per memorizzare le spese durante la sessione
if 'spese' not in st.session_state:
    st.session_state.spese = pd.DataFrame(columns=["categoria", "descrizione", "importo"])

# Form per inserire nuova spesa
with st.form("inserisci_spesa"):
    categoria = st.selectbox("Categoria", ["Cibo", "Affitto", "Trasporti", "Svago", "Altro"])
    descrizione = st.text_input("Descrizione")
    importo = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Aggiungi spesa")

    if submitted:
        nuova_spesa = {"categoria": categoria, "descrizione": descrizione, "importo": importo}
        st.session_state.spese = pd.concat([st.session_state.spese, pd.DataFrame([nuova_spesa])], ignore_index=True)
        st.success("Spesa aggiunta!")

# Mostra le spese inserite
st.write("📊 Spese registrate:")
st.dataframe(st.session_state.spese)

# Calcolo totale
totale = st.session_state.spese["importo"].sum()
st.metric("Totale spese", f"{totale:.2f} €")

# Grafico a torta per categoria
if not st.session_state.spese.empty:
    fig = px.pie(st.session_state.spese, values="importo", names="categoria", title="Distribuzione per categoria")
    st.plotly_chart(fig)
else:
    st.info("Inserisci spese per visualizzare il grafico.")
