import streamlit as st
import google.generativeai as genai

st.title("Diagnóstico de Modelos Disponibles")

try:
    # 1. Configurar
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 2. Listar modelos
    st.write("Buscando modelos compatibles...")
    models = genai.list_models()
    
    # 3. Mostrar lo que SÍ funciona
    st.write("### Modelos encontrados:")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"Nombre del modelo: {m.name}")
            
except Exception as e:
    st.error(f"Error al conectar: {e}")
