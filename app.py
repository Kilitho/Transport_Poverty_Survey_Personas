import streamlit as st

def init_state():
    if "data" not in st.session_state:
        st.session_state.data = {
            "edad": 0,
            "ninos": 0,
            "adultos": 0,
            "trabajo": {},
            "salud": {}
        }

init_state()

st.title("Encuesta sobre pobreza en el transporte")

st.write("""
La pobreza en el transporte se refiere a la dificultad de acceder a servicios esenciales
debido a limitaciones económicas o de movilidad.
""")

if st.button("Comenzar encuesta"):
    st.switch_page("pages/1_Datos_generales.py")