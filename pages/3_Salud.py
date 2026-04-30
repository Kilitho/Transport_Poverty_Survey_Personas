import streamlit as st

st.set_page_config(page_title="Encuesta", layout="wide")

st.title("Salud")

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = {}

if "acumulados" not in st.session_state:
    st.session_state.acumulados = {
        "trayectos_totales": 0,
        "trayectos_largos": 0
    }

acum = st.session_state.acumulados

# --- PREFERENCIAS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔢 Frecuencia")
    frecuencia = st.slider("Visitas al mes", 0, 20, 1)

with col2:
    st.subheader("⏳ Tiempo razonable")
    tiempo_razonable = st.slider("Minutos", 5, 120, 30, step=5)

# --- TRANSPORTES ---
st.subheader("Tiempo por transporte")

transportes = st.session_state.data.get("transportes", [])
resultados = {}

iconos = {
    "Coche/Moto": "🚗",
    "Bicicleta": "🚲",
    "Caminar": "🚶",
    "Transporte público": "🚌"
}

errores = False

for t in ["Coche/Moto", "Bicicleta", "Caminar", "Transporte público"]:
    if t in transportes:
        val = st.number_input(
            f"{iconos[t]} {t} (min)",
            min_value=1,
            value=None,
            placeholder="Introduce tiempo..."
        )
        resultados[t] = val

        if val is None:
            errores = True

if errores:
    st.error("⚠️ Debes completar todos los tiempos")

# --- SIDEBAR ---
st.sidebar.title("Resumen salud")

cumplen = 0
for t, tiempo in resultados.items():
    if tiempo is not None and tiempo <= tiempo_razonable:
        st.sidebar.success(f"{t}: {tiempo} min ✔")
        cumplen += 1
    elif tiempo is not None:
        st.sidebar.error(f"{t}: {tiempo} min ✖")

# --- CÁLCULOS ---
valores_validos = [v for v in resultados.values() if v is not None]

if len(valores_validos) > 0:

    tiempo_min = min(valores_validos)
    tiempo_total_horas = (tiempo_min * frecuencia) / 60

    hay_eficiente = any(v <= tiempo_razonable for v in valores_validos)

    trayectos_totales = frecuencia
    trayectos_largos = 0 if hay_eficiente else frecuencia

    total_acum = acum["trayectos_totales"] + trayectos_totales
    largos_acum = acum["trayectos_largos"] + trayectos_largos

    # --- MÉTRICAS ---
    st.subheader("Resumen salud")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tiempo total mensual", f"{tiempo_total_horas:.1f} h")

    with col2:
        st.metric("Medios eficientes", f"{cumplen}/{len(valores_validos)}")

    with col3:
        st.metric("Trayectos demasiado largos", largos_acum)

    st.markdown("### 🚦 Eficiencia total acumulada")

    st.write(
        f"**{total_acum - largos_acum} / {total_acum} trayectos cumplen el tiempo razonable**"
    )

# --- GUARDAR ---
st.session_state.data["salud"] = {
    "frecuencia": frecuencia,
    "tiempos": resultados,
    "tiempo_razonable": tiempo_razonable
}

# --- BOTÓN ---
if st.button("Ver resultados"):
    if errores:
        st.warning("Completa todos los campos antes de continuar")
    else:
        st.session_state.acumulados["trayectos_totales"] += frecuencia

        if not any(v <= tiempo_razonable for v in valores_validos):
            st.session_state.acumulados["trayectos_largos"] += frecuencia

        st.switch_page("pages/4_Resultados.py")

# --- PROGRESO ABAJO ---
st.progress(0.75)