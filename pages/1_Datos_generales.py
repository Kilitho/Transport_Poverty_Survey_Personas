"""import streamlit as st

st.title("Datos generales")

st.session_state.data["edad"] = st.number_input("Edad", 0, 100)

st.session_state.data["situacion"] = st.selectbox(
    "Situación actual",
    ["Estudia", "Trabaja", "Jubilado", "Desempleado"]
)

st.session_state.data["ninos"] = st.number_input("Menores a cargo", 0)
st.session_state.data["adultos"] = st.number_input("Adultos a cargo", 0)

st.session_state.data["transportes"] = st.multiselect(
    "Transportes",
    ["Caminar", "Bicicleta", "Transporte público", "Coche/Moto"]
)


    
if st.button("Siguiente"):
    st.switch_page("pages/2_Trabajo.py")
    
"""

import streamlit as st

st.set_page_config(page_title="Encuesta", layout="wide")

st.title("Datos generales")

# Barra de progreso (ejemplo: 25%)
st.progress(0.25)

# --- FILA SUPERIOR ---
col1, col2 = st.columns(2)

with col1:
    edad = st.number_input("Edad", 0, 100)

with col2:
    situacion = st.selectbox(
        "Situación actual",
        ["Estudia", "Trabaja", "Jubilado", "Desempleado"]
    )

# --- FILA INFERIOR ---
ninos = st.number_input("Menores a cargo", 0)
adultos = st.number_input("Adultos a cargo", 0)

transportes = st.multiselect(
    "Transportes que usas habitualmente",
    ["Caminar", "Bicicleta", "Transporte público", "Coche/Moto"]
)

# Guardar en session_state
st.session_state.data["edad"] = edad
st.session_state.data["situacion"] = situacion
st.session_state.data["ninos"] = ninos
st.session_state.data["adultos"] = adultos
st.session_state.data["transportes"] = transportes

if st.button("Siguiente"):
    st.switch_page("pages/2_Trabajo.py")