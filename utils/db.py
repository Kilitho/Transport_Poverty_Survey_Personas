from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["https://emujzqjcyvdubpwecbkt.supabase.co"]
    key = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtdWp6cWpjeXZkdWJwd2VjYmt0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczODE1NDQsImV4cCI6MjA5Mjk1NzU0NH0.h6SrQGCGNJ6Ednls04z4m1NIkdctOyiEgIjGq0yJm5o"]
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