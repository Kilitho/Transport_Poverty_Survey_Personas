from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Survey", layout="wide")

# --- BIGGER TEXT ---
st.markdown("""
<style>
label, .stMarkdown {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("General Information")

st.progress(0.25)

# --- TOP ROW ---
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 0, 100, 30)

with col2:
    situation = st.selectbox(
        "Current situation",
        ["Student", "Employed", "Retired", "Unemployed"]
    )

# --- LOCATION ---
st.subheader("Where do you live?")


image_path = Path("Images/Urban_rural.png")

st.image(image_path, width=450)

zone = st.radio(
    "Select your area type",
    ["A: Urban", "B: Peri-urban", "C: Rural"]
)

country = st.text_input("Which country do you live in?")

# --- TRANSPORT FIRST ---
transport_modes = st.multiselect(
    "Which transport modes do you usually use?",
    ["Walking", "Bicycle", "Public transport", "Car/Motorbike"]
)

# --- DEPENDENTS ---
children = st.number_input("Children in care", 0)
adults = st.number_input("Adults in care", 0)

# --- SAVE ---
st.session_state.data.update({
    "age": age,
    "situation": situation,
    "children": children,
    "adults": adults,
    "transport_modes": transport_modes,
    "zone": zone,
    "country": country
})

# --- VALIDATION ---
error = False

if st.button("Next"):
    if len(transport_modes) == 0:
        error = True
    else:
        st.switch_page("pages/2_Trabajo.py")

if error:
    st.error("⚠️ Please select at least one transport mode")