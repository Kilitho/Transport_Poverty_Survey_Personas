from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Survey", layout="wide")

# --- GLOBAL STYLE (bigger text) ---
st.markdown("""
<style>
label, .stMarkdown, .stRadio, .stSelectbox {
    font-size: 18px !important;
}

.big-label {
    font-size: 22px !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("General Information")

# --- SESSION STATE ---
if "data" not in st.session_state:
    st.session_state.data = {}

# =========================================================
# TOP ROW (AGE + SITUATION BIGGER)
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="big-label">👤 Personal situation</div>', unsafe_allow_html=True)
    situation = st.selectbox(
        "",
        [
            "Student",
            "Employed",
            "Student & Working",
            "Retired",
            "Unemployed"
        ],
        index=None
    )


with col2:
    st.markdown('<div class="big-label">🎂 Age</div>', unsafe_allow_html=True)
    age = st.slider("", 0, 100, 30)


# =========================================================
# LOCATION INSIDE CITY
# =========================================================

st.subheader("Where do you live inside your city?")

image_path = Path("Images/Urban_rural.png")
st.image(image_path, width=450)

zone = st.radio(
    "Select your area type",
    ["Urban", "Peri-urban", "Rural"],
    index=None
)

# =========================================================
# COUNTRY (NO PRESELECTED VALUE)
# =========================================================

eu_countries = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Slovenia", "Spain", "Sweden"
]

country = st.selectbox(
    "Which country do you live in?",
    [""] + sorted(eu_countries) + ["Other"],
    index=0
)

if country == "Other":
    country = st.text_input("Please specify your country")

# =========================================================
# TRANSPORT MODES
# =========================================================

transport_modes = st.multiselect(
    "Which transport modes do you usually use?",
    ["Walking", "Bicycle", "Public transport", "Car/Motorbike"]
)

# =========================================================
# DEPENDENTS
# =========================================================

children = st.number_input("Children in care", 0)
adults = st.number_input("Adults in care", 0)

# =========================================================
# SAVE DATA
# =========================================================

st.session_state.data.update({
    "age": age,
    "situation": situation,
    "children": children,
    "adults": adults,
    "transport_modes": transport_modes,
    "zone": zone,
    "country": country
})

# =========================================================
# VALIDATION + NEXT BUTTON
# =========================================================

error = False
missing_fields = []

if st.button("Next"):

    if len(transport_modes) == 0:
        error = True
        missing_fields.append("transport modes")

    if age is None:
        error = True
        missing_fields.append("age")

    if situation is None:
        error = True
        missing_fields.append("situation")

    if zone is None:
        error = True
        missing_fields.append("location type")

    if country == "" or country is None:
        error = True
        missing_fields.append("country")

    if error:
        st.error("⚠️ Please complete all required fields before continuing.")
        st.write("Missing:", ", ".join(missing_fields))
    else:
        st.switch_page("pages/2_Trabajo.py")

# =========================================================
# PROGRESS BAR (BOTTOM)
# =========================================================

st.markdown("---")
st.progress(0.25)