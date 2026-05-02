import streamlit as st

def init_state():
    if "data" not in st.session_state:
        st.session_state.data = {}

    if "acumulados" not in st.session_state:
        st.session_state.acumulados = {
            "total_trips": 0,
            "efficient_trips": 0,
            "total_hours": 0
        }

    st.session_state.data.setdefault("trabajo", {})
    st.session_state.data.setdefault("salud", {})
    st.session_state.data.setdefault("supermercado", {})

init_state()

st.title("Transport Poverty Survey")

st.markdown("""
<div style="font-size:18px;">
Transport poverty refers to the difficulty of accessing essential services 
due to economic or mobility limitations.
</div>
""", unsafe_allow_html=True)

if st.button("Start survey"):
    st.switch_page("pages/1_Datos_generales.py")