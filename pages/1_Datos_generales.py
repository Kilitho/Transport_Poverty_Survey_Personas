import streamlit as st

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
    ["Coche", "Bici", "Andando", "Transporte público"]
)


    
if st.button("Siguiente"):
    st.switch_page("pages/2_Trabajo.py")