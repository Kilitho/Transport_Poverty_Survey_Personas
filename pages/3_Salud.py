import streamlit as st

st.title("Salud")

st.session_state.data["salud"] = {
    "frecuencia": st.number_input("Visitas al mes", 0, value=1),
    "coche": st.number_input("Tiempo coche", 0),
    "bici": st.number_input("Tiempo bici", 0),
    "andando": st.number_input("Tiempo andando", 0)
}

if st.button("Ver resultados"):
    st.switch_page("pages/4_Resultados.py")