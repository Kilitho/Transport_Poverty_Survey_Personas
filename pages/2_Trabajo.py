"""
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
"""

    
    
import streamlit as st

# Configuración general
st.set_page_config(page_title="Encuesta", layout="wide")

# Estilo visual
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

st.title("Desplazamientos al trabajo")

# Barra de progreso (ajusta según número total de páginas)
st.progress(0.5)

# Asegurar session_state
if "data" not in st.session_state:
    st.session_state.data = {}

data_prev = st.session_state.data

# --- PREGUNTAS PRINCIPALES ---
st.subheader("⏱️ Preferencias de tiempo")

col1, col2 = st.columns(2)

with col1:
    tiempo_razonable = st.slider(
        "⏳ Tiempo razonable para llegar (min)",
        min_value=5,
        max_value=120,
        value=30,
        step=5
    )

with col2:
    frecuencia = st.slider(
        "🔁 Veces que vas al trabajo al mes",
        min_value=0,
        max_value=40,
        value=20,
        step=1
    )

# --- TRANSPORTES DINÁMICOS ---
st.subheader("Tiempo por transporte")

transportes = data_prev.get("transportes", [])

col1, col2 = st.columns(2)

resultados = {}

with col1:
    if "Coche/Moto" in transportes:
        resultados["Coche/Moto"] = st.number_input("Tiempo en coche (min)", 0)

    if "Bicicleta" in transportes:
        resultados["Bicicleta"] = st.number_input("Tiempo en bici (min)", 0)

with col2:
    if "Caminar" in transportes:
        resultados["Caminar"] = st.number_input("Tiempo andando (min)", 0)

    if "Transporte público" in transportes:
        resultados["Transporte público"] = st.number_input("Tiempo en transporte público (min)", 0)

# --- SIDEBAR: VALIDACIÓN ---
st.sidebar.title("Resumen de trayectos")

cumplen = 0
total = len(resultados)

for transporte, tiempo in resultados.items():
    if tiempo <= tiempo_razonable:
        st.sidebar.success(f"{transporte}: {tiempo} min ✔")
        cumplen += 1
    else:
        st.sidebar.error(f"{transporte}: {tiempo} min ✖")

# Barra de cumplimiento
if total > 0:
    porcentaje = cumplen / total
    st.sidebar.progress(porcentaje)
    st.sidebar.write(f"{cumplen} de {total} cumplen el tiempo razonable")

# --- MÉTRICAS EXTRA (opcional pero queda pro) ---
if total > 0:
    tiempo_total = sum(resultados.values()) * frecuencia

    st.subheader("Resumen mensual")
    colA, colB = st.columns(2)

    with colA:
        st.metric("Tiempo total mensual", f"{tiempo_total} min")

    with colB:
        st.metric("Trayectos eficientes", f"{cumplen}/{total}")

# --- GUARDAR DATOS ---
st.session_state.data["trabajo"] = {
    "frecuencia": frecuencia,
    "tiempos": resultados,
    "tiempo_razonable": tiempo_razonable
}

# --- BOTÓN SIGUIENTE ---
if st.button("Siguiente"):
    st.switch_page("pages/3_Salud.py")