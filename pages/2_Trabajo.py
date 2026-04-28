import streamlit as st

st.title("Desplazamientos al trabajo")

st.session_state.data["trabajo"] = {
    "frecuencia": st.number_input(
        "¿Cuántas veces vas al trabajo al mes?",
        min_value=0,
        value=20
    ),
    "coche": st.number_input("Tiempo en coche (minutos)", 0),
    "bici": st.number_input("Tiempo en bici (minutos)", 0),
    "andando": st.number_input("Tiempo andando (minutos)", 0)
}

if st.button("Siguiente"):
    st.switch_page("pages/3_Salud.py")