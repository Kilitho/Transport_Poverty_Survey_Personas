from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)



    
    
def guardar_respuesta(data):
    supabase = get_client()

    trabajo = data.get("trabajo") or {}
    salud = data.get("salud") or {}

    response = supabase.table("respuestas").insert({
        "edad": int(data.get("edad") or 0),
        "situacion": data.get("situacion") or "",
        "ninos": int(data.get("ninos") or 0),
        "adultos": int(data.get("adultos") or 0),

        "transportes": ", ".join(data.get("transportes") or []),

        "trabajo_freq": int(trabajo.get("frecuencia") or 0),
        "trabajo_coche": int(trabajo.get("coche") or 0),
        "trabajo_bici": int(trabajo.get("bici") or 0),
        "trabajo_andando": int(trabajo.get("andando") or 0),

        "salud_freq": int(salud.get("frecuencia") or 0),
        "salud_coche": int(salud.get("coche") or 0),
        "salud_bici": int(salud.get("bici") or 0),
        "salud_andando": int(salud.get("andando") or 0),
    }).execute()

    return response