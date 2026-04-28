import streamlit as st
from utils.calculos import calcular_indice

st.title("Resultado")

data = st.session_state.data

indice = calcular_indice(data)

st.metric("Índice de vulnerabilidad", f"{indice}/100")

if indice < 30:
    st.success("Baja vulnerabilidad")
elif indice < 60:
    st.warning("Media")
else:
    st.error("Alta")

st.write(data)
