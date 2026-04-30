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

st.set_page_config(page_title="Encuesta", layout="wide")

# --- ESTILO ---
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
st.progress(0.5)

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = {}

data_prev = st.session_state.data

# --- PREFERENCIAS ---
st.subheader("⏱️ Preferencias de tiempo")

col1, col2 = st.columns(2)

with col1:
    tiempo_razonable = st.slider(
        "⏳ Tiempo razonable (min)",
        5, 120, 30, step=5
    )

with col2:
    frecuencia = st.slider(
        "🔁 Veces al mes",
        0, 40, 20
    )

# --- TRANSPORTES (VERTICAL) ---
st.subheader("🚶 Tiempo por transporte")

transportes = data_prev.get("transportes", [])
resultados = {}

for t in ["Coche/Moto", "Bicicleta", "Caminar", "Transporte público"]:
    if t in transportes:
        resultados[t] = st.number_input(f"{t} (min)", 0)

# --- SIDEBAR ---
st.sidebar.title("Resumen de trayectos")

cumplen_medios = 0
total_medios = len(resultados)

for transporte, tiempo in resultados.items():
    if tiempo <= tiempo_razonable:
        st.sidebar.success(f"{transporte}: {tiempo} min ✔")
        cumplen_medios += 1
    else:
        st.sidebar.error(f"{transporte}: {tiempo} min ✖")

if total_medios > 0:
    st.sidebar.progress(cumplen_medios / total_medios)

# --- CÁLCULOS IMPORTANTES ---
viajes_totales = frecuencia * total_medios
viajes_eficientes = 0

for tiempo in resultados.values():
    if tiempo <= tiempo_razonable:
        viajes_eficientes += frecuencia

viajes_largos = viajes_totales - viajes_eficientes

# --- MÉTRICAS ---
if total_medios > 0:
    st.subheader("📊 Resumen mensual")

    colA, colB, colC = st.columns(3)

    with colA:
        tiempo_total = sum(resultados.values()) * frecuencia
        st.metric("Tiempo total mensual", f"{tiempo_total} min")

    with colB:
        st.metric(
            "Medios de transporte eficientes",
            f"{cumplen_medios}/{total_medios}"
        )

    with colC:
        st.metric(
            "Trayectos demasiado largos",
            viajes_largos
        )

    # --- MÉTRICA AVANZADA (LO QUE PEDÍAS) ---
    st.markdown("### 🚦 Eficiencia total de trayectos")

    st.write(
        f"**{viajes_eficientes} / {viajes_totales} trayectos cumplen el tiempo razonable**"
    )

# --- GUARDAR ---
st.session_state.data["trabajo"] = {
    "frecuencia": frecuencia,
    "tiempos": resultados,
    "tiempo_razonable": tiempo_razonable
}

if st.button("Siguiente"):
    st.switch_page("pages/3_Salud.py")