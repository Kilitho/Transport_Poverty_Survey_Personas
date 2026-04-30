"""import streamlit as st

st.title("Salud")

st.session_state.data["salud"] = {
    "frecuencia": st.number_input("Visitas al mes", 0, value=1),
    "coche": st.number_input("Tiempo coche", 0),
    "bici": st.number_input("Tiempo bici", 0),
    "andando": st.number_input("Tiempo andando", 0)
}

if st.button("Ver resultados"):
    st.switch_page("pages/4_Resultados.py")"""
    

import streamlit as st

st.set_page_config(page_title="Encuesta", layout="wide")

st.title("Salud")
st.progress(0.75)

if "data" not in st.session_state:
    st.session_state.data = {}

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
        "🏥 Visitas al mes",
        0, 20, 1
    )

# --- TRANSPORTES ---
st.subheader("🚶 Tiempo por transporte")

transportes = st.session_state.data.get("transportes", [])
resultados = {}

for t in ["Coche/Moto", "Bicicleta", "Caminar", "Transporte público"]:
    if t in transportes:
        resultados[t] = st.number_input(f"{t} (min)", 0)

# --- SIDEBAR ---
st.sidebar.title("Resumen salud")

cumplen = 0
total = len(resultados)

for transporte, tiempo in resultados.items():
    if tiempo <= tiempo_razonable:
        st.sidebar.success(f"{transporte}: {tiempo} min ✔")
        cumplen += 1
    else:
        st.sidebar.error(f"{transporte}: {tiempo} min ✖")

if total > 0:
    st.sidebar.progress(cumplen / total)

# --- CÁLCULOS ---
viajes_totales = frecuencia * total
viajes_eficientes = sum(
    frecuencia for t in resultados.values() if t <= tiempo_razonable
)

# --- MÉTRICAS ---
if total > 0:
    st.subheader("📊 Resumen salud")

    col1, col2, col3 = st.columns(3)

    with col1:
        tiempo_total = sum(resultados.values()) * frecuencia
        st.metric("Tiempo total mensual", f"{tiempo_total} min")

    with col2:
        st.metric("Medios eficientes", f"{cumplen}/{total}")

    with col3:
        st.metric("Trayectos largos", viajes_totales - viajes_eficientes)

    st.write(
        f"**{viajes_eficientes} / {viajes_totales} trayectos dentro del tiempo razonable**"
    )

# --- GUARDAR ---
st.session_state.data["salud"] = {
    "frecuencia": frecuencia,
    "tiempos": resultados,
    "tiempo_razonable": tiempo_razonable
}

if st.button("Ver resultados"):
    st.switch_page("pages/4_Resultados.py")