import streamlit as st

st.set_page_config(page_title="Encuesta", layout="wide")

st.title("Salud")

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
    frecuencia = st.slider("Visitas al mes", 0, 20, 1)

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

# --- CÁLCULOS ---
valores_validos = [v for v in resultados.values() if v is not None]

if len(valores_validos) > 0:

    tiempo_min = min(valores_validos)
    horas_pagina = (tiempo_min * frecuencia) / 60

    hay_eficiente = any(v <= tiempo_razonable for v in valores_validos)

    total_acum = acum["trayectos_totales"] + frecuencia
    cumplen_acum = acum["trayectos_cumplen"] + (frecuencia if hay_eficiente else 0)
    horas_acum = acum["horas_totales"] + horas_pagina

    # --- MÉTRICAS ---
    st.subheader("Resumen salud")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tiempo total", f"{horas_pagina:.1f} h")

    with col2:
        st.metric("Medios eficientes", f"{sum(v <= tiempo_razonable for v in valores_validos)}/{len(valores_validos)}")

    with col3:
        st.metric("Trayectos largos", total_acum - cumplen_acum)

    st.markdown("### 📊 Acumulado global")

    st.write(f"**Horas totales acumuladas: {horas_acum:.1f} h**")
    st.write(f"**{cumplen_acum} / {total_acum} trayectos cumplen el tiempo razonable**")

# --- GUARDADO ---
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

        if any(v <= tiempo_razonable for v in valores_validos):
            st.session_state.acumulados["trayectos_cumplen"] += frecuencia

        st.session_state.acumulados["horas_totales"] += horas_pagina

        st.switch_page("pages/4_Resultados.py")

# --- PROGRESO ---
st.progress(0.75)