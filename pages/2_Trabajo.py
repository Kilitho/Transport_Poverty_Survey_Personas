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

st.title("Desplazamientos al trabajo")

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = {}

if "acumulados" not in st.session_state:
    st.session_state.acumulados = {
        "trayectos_totales": 0,
        "trayectos_largos": 0
    }

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
st.sidebar.title("Resumen")

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

    acum = st.session_state.acumulados

    total_acum = acum["trayectos_totales"] + trayectos_totales
    largos_acum = acum["trayectos_largos"] + trayectos_largos

    # --- MÉTRICAS ---
    st.subheader("Resumen mensual")

    colA, colB, colC = st.columns(3)

    with colA:
        st.metric("Tiempo total mensual", f"{tiempo_total_horas:.1f} h")

    with colB:
        st.metric("Medios eficientes", f"{cumplen}/{len(valores_validos)}")

    with colC:
        st.metric("Trayectos demasiado largos", largos_acum)

    st.markdown("### 🚦 Eficiencia total")
    st.write(f"**{total_acum - largos_acum} / {total_acum} trayectos cumplen el tiempo razonable**")

# --- GUARDAR ---
st.session_state.data["trabajo"] = {
    "frecuencia": frecuencia,
    "tiempos": resultados,
    "tiempo_razonable": tiempo_razonable
}

# --- BOTÓN ---
if st.button("Siguiente"):
    if errores:
        st.warning("Completa todos los campos antes de continuar")
    else:
        st.session_state.acumulados["trayectos_totales"] += frecuencia

        if not any(v <= tiempo_razonable for v in valores_validos):
            st.session_state.acumulados["trayectos_largos"] += frecuencia

        st.switch_page("pages/3_Salud.py")

# --- PROGRESO ABAJO ---
st.progress(0.5)