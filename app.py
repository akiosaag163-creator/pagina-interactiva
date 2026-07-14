import streamlit as st
import google.generativeai as genai

# --- AQUÍ EMPIEZA LA CONFIGURACIÓN ---
st.set_page_config(page_title="Mentor Científico", page_icon="🎓")

# Esto es lo que verifica si tu clave funciona
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    # Si quieres ver si funcionó, puedes poner esta línea:
    # st.success("¡Conexión establecida!") 
except Exception as e:
    st.error("Error: Revisa que tu API KEY esté bien escrita en los Secrets.")
    st.stop()
# --- AQUÍ TERMINA LA CONFIGURACIÓN ---

# A partir de aquí sigue tu código normal (el título, el chat, etc.)
st.title("🎓 Mentor de Ciencias y Matemáticas")
