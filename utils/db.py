from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)



    
def guardar_respuesta(data):
    supabase = get_client()

    try:
        response = supabase.table("respuestas").insert({
            "edad": int(data.get("edad") or 0),
            "situacion": data.get("situacion"),
            "ninos": int(data.get("ninos") or 0),
            "adultos": int(data.get("adultos") or 0),

            "transportes": ", ".join(data.get("transportes") or []),

            "trabajo_freq": int(data.get("trabajo", {}).get("frecuencia") or 0),
            "trabajo_coche": int(data.get("trabajo", {}).get("coche") or 0),
            "trabajo_bici": int(data.get("trabajo", {}).get("bici") or 0),
            "trabajo_andando": int(data.get("trabajo", {}).get("andando") or 0),

            "salud_freq": int(data.get("salud", {}).get("frecuencia") or 0),
            "salud_coche": int(data.get("salud", {}).get("coche") or 0),
            "salud_bici": int(data.get("salud", {}).get("bici") or 0),
            "salud_andando": int(data.get("salud", {}).get("andando") or 0),
        }).execute()

        return response

    except Exception as e:
        import streamlit as st
        st.error(str(e))
        raise