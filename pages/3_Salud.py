import streamlit as st

st.set_page_config(page_title="Survey", layout="wide")

st.title("Hospital trips")

data_prev = st.session_state.data
acum = st.session_state.acumulados

col1, col2 = st.columns(2)

with col1:
    frequency = st.slider("How many times per month do you go to the hospital?", 0, 20, 1)

with col2:
    reasonable_time = st.slider("Reasonable travel time (min)", 5, 120, 30, step=5)

st.subheader("Travel time by transport")

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
        results[t] = st.number_input(f"{icons[t]} {t} (min)", min_value=1, value=None)

values = [v for v in results.values() if v is not None]
errors = len(values) == 0 or any(v is None for v in results.values())

if len(values) > 0:

    min_time = min(values)
    hours_page = (min_time * frequency) / 60
    efficient = any(v <= reasonable_time for v in values)

    total_acum = acum["total_trips"] + frequency
    efficient_acum = acum["efficient_trips"] + (frequency if efficient else 0)
    hours_acum = acum["total_hours"] + hours_page

    st.subheader("Monthly summary for hospitals")

    colA, colB = st.columns(2)
    colA.metric("Total time spent going to hospital", f"{hours_page:.1f} h")
    colB.metric("Number of transport that allow you to reach hospital in reasonable time", f"{sum(v <= reasonable_time for v in values)}/{len(values)}")

    st.markdown("### 📊 Global monthly accumulation")
    
    st.success("""
### 🌍 Global accumulation

You can now see that this considers the work trips + the hospital trips. 
""")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total hours spent in transport", f"{hours_acum:.1f} h")
    col2.metric("Essential trips within reasonable time / Essential trips", f"{efficient_acum} / {total_acum}")
    col3.metric("Essential trips that take too long", total_acum - efficient_acum)

if st.button("Next"):
    if errors:
        st.warning("⚠️ Complete all fields")
    else:
        st.session_state.acumulados["total_trips"] += frequency
        if efficient:
            st.session_state.acumulados["efficient_trips"] += frequency
        st.session_state.acumulados["total_hours"] += hours_page

        st.switch_page("pages/4_Supermarket.py")

st.progress(0.75)