import streamlit as st
import google.generativeai as genai

st.title("Prueba de Diagnóstico")

try:
    # Intentamos configurar la API
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    
    # Probamos una respuesta súper simple
    response = model.generate_content("Hola, dime 'Hola' si funcionas.")
    st.write(response.text)
    
except Exception as e:
    st.error(f"Error técnico detallado: {e}")
