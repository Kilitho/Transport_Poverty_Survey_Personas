import streamlit as st

st.set_page_config(page_title="Encuesta", layout="wide")

st.title("Desplazamientos al trabajo")

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = {}

if "acumulados" not in st.session_state:
    st.session_state.acumulados = {
        "trayectos_totales": 0,
        "trayectos_cumplen": 0,
        "horas_totales": 0
    }

acum = st.session_state.acumulados
data_prev = st.session_state.data

# --- PREFERENCIAS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔢 Frecuencia")
    frecuencia = st.slider("Veces al mes", 0, 40, 20)

with col2:
    st.subheader("⏳ Tiempo razonable")
    tiempo_razonable = st.slider("Minutos", 5, 120, 30, step=5)

# --- TRANSPORTES ---
st.subheader("Tiempo por transporte")

transportes = data_prev.get("transportes", [])
resultados = {}

iconos = {
    "Coche/Moto": "🚗",
    "Bicicleta": "🚲",
    "Caminar": "🚶",
    "Transporte público": "🚌"
}

for t in ["Coche/Moto", "Bicicleta", "Caminar", "Transporte público"]:
    if t in transportes:
        resultados[t] = st.number_input(
            f"{iconos[t]} {t} (min)",
            min_value=1,
            value=None,
            placeholder="Introduce tiempo..."
        )

# --- VALIDACIÓN SOLO AL ENVIAR ---
valores_validos = [v for v in resultados.values() if v is not None]
errores = len(valores_validos) == 0 or any(v is None for v in resultados.values())

# --- CÁLCULOS ---
if len(valores_validos) > 0:

    tiempo_min = min(valores_validos)
    horas_pagina = (tiempo_min * frecuencia) / 60

    hay_eficiente = any(v <= tiempo_razonable for v in valores_validos)

    total_acum = acum["trayectos_totales"] + frecuencia
    cumplen_acum = acum["trayectos_cumplen"] + (frecuencia if hay_eficiente else 0)
    horas_acum = acum["horas_totales"] + horas_pagina

    # --- RESUMEN ---
    st.subheader("Resumen mensual")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Tiempo total", f"{horas_pagina:.1f} h")

    with colB:
        st.metric(
            "Medios eficientes",
            f"{sum(v <= tiempo_razonable for v in valores_validos)}/{len(valores_validos)}"
        )

    # --- ACUMULADO GLOBAL ---
    st.markdown("### 📊 Acumulado global")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Horas totales acumuladas", f"{horas_acum:.1f} h")

    with col2:
        st.metric(
            "Trayectos dentro del tiempo razonable",
            f"{cumplen_acum} / {total_acum}"
        )

    with col3:
        st.metric(
            "Trayectos largos",
            total_acum - cumplen_acum
        )

# --- BOTÓN ---
if st.button("Siguiente"):

    if errores:
        st.warning("⚠️ Completa todos los tiempos antes de continuar")
    else:
        st.session_state.acumulados["trayectos_totales"] += frecuencia

        if hay_eficiente:
            st.session_state.acumulados["trayectos_cumplen"] += frecuencia

        st.session_state.acumulados["horas_totales"] += horas_pagina

        st.switch_page("pages/3_Salud.py")

# --- PROGRESO ---
st.progress(0.5)