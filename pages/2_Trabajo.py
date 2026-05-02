import streamlit as st

st.set_page_config(page_title="Survey", layout="wide")

st.title("Work trips")

data_prev = st.session_state.data
acum = st.session_state.acumulados

# --- PREFERENCES ---
col1, col2 = st.columns(2)

with col1:
    frequency = st.slider("How many times per month do you go to work?", 0, 40, 20)

with col2:
    reasonable_time = st.slider("What travel time is reasonable for this trip? (min)", 5, 120, 30, step=5)

# --- TRANSPORT ---
st.subheader("How long does it take you to get to work by...")

transport_modes = data_prev.get("transport_modes", [])
results = {}

icons = {
    "Car/Motorbike": "🚗",
    "Bicycle": "🚲",
    "Walking": "🚶",
    "Public transport": "🚌"
}

for t in ["Car/Motorbike", "Bicycle", "Walking", "Public transport"]:
    if t in transport_modes:
        results[t] = st.number_input(
            f"{icons[t]} {t} (min)",
            min_value=1,
            value=None,
            placeholder="Enter time..."
        )

# --- VALIDATION ---
values = [v for v in results.values() if v is not None]
errors = len(values) == 0 or any(v is None for v in results.values())

# --- CALCULATIONS ---
if len(values) > 0:

    min_time = min(values)
    hours_page = (min_time * frequency) / 60

    efficient = any(v <= reasonable_time for v in values)

    total_acum = acum["total_trips"] + frequency
    efficient_acum = acum["efficient_trips"] + (frequency if efficient else 0)
    hours_acum = acum["total_hours"] + hours_page

    # --- SUMMARY ---
    st.subheader("Monthly summary")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Total time spent", f"{hours_page:.1f} h")

    with colB:
        st.metric("Efficient transport modes", f"{sum(v <= reasonable_time for v in values)}/{len(values)}")

    # --- GLOBAL ---
    st.markdown("### 📊 Global accumulation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total hours", f"{hours_acum:.1f} h")

    with col2:
        st.metric("Trips within reasonable time", f"{efficient_acum} / {total_acum}")

    with col3:
        st.metric("Long trips", total_acum - efficient_acum)

# --- BUTTON ---
if st.button("Next"):
    if errors:
        st.warning("⚠️ Please complete all transport times")
    else:
        st.session_state.acumulados["total_trips"] += frequency

        if efficient:
            st.session_state.acumulados["efficient_trips"] += frequency

        st.session_state.acumulados["total_hours"] += hours_page

        st.switch_page("pages/3_Salud.py")

st.progress(0.5)