import streamlit as st

def init_state():
    if "data" not in st.session_state:
        st.session_state.data = {}

    # aseguramos claves siempre existentes
    st.session_state.data.setdefault("edad", 0)
    st.session_state.data.setdefault("ninos", 0)
    st.session_state.data.setdefault("adultos", 0)
    st.session_state.data.setdefault("trabajo", {})
    st.session_state.data.setdefault("salud", {})

init_state()

st.title("Encuesta sobre pobreza en el transporte")

st.write("""
La pobreza en el transporte se refiere a la dificultad de acceder a servicios esenciales
debido a limitaciones económicas o de movilidad.
""")

if st.button("Comenzar encuesta"):
    st.switch_page("pages/1_Datos_generales.py")