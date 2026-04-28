from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)



def guardar_respuesta(data):
    supabase = get_client()

    supabase.table("respuestas").insert({
        "edad": data.get("edad"),
        "situacion": data.get("situacion"),
        "ninos": data.get("ninos"),
        "adultos": data.get("adultos"),
        "transportes": ", ".join(data.get("transportes", [])),

        "trabajo_freq": data.get("trabajo", {}).get("frecuencia"),
        "trabajo_coche": data.get("trabajo", {}).get("coche"),
        "trabajo_bici": data.get("trabajo", {}).get("bici"),
        "trabajo_andando": data.get("trabajo", {}).get("andando"),

        "salud_freq": data.get("salud", {}).get("frecuencia"),
        "salud_coche": data.get("salud", {}).get("coche"),
        "salud_bici": data.get("salud", {}).get("bici"),
        "salud_andando": data.get("salud", {}).get("andando"),
    }).execute()