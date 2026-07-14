import streamlit as st
import google.generativeai as genai

st.title("Prueba de Comunicación")

# Configuración básica
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

if st.button("Probar conexión"):
    try:
        response = model.generate_content("Responde solo con la palabra: FUNCIONA")
        st.write("Respuesta del bot: " + response.text)
    except Exception as e:
        st.error(f"Error detectado: {e}")
