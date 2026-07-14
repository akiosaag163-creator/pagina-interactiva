import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")
st.title("🎓 Mentor Estelar: Quiz Inteligente")

# Configuración API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
    st.session_state.evaluado = False

# Input del usuario para generar quiz
if prompt := st.chat_input("Escribe 'Quiz de [Tema]'"):
    st.session_state.evaluado = False
    with st.spinner('El mentor está creando tu quiz...'):
        instruccion = f"""Genera una pregunta de quiz sobre {prompt}. 
        Dame el formato exacto:
        PREGUNTA: [La pregunta]
        A) [Opción]
        B) [Opción]
        C) [Opción]
        CORRECTA: [La letra de la opción correcta]"""
        
        response = model.generate_content(instruccion)
        st.session_state.quiz_data = response.text

# Mostrar y evaluar el quiz
if st.session_state.quiz_data:
    st.markdown(st.session_state.quiz_data.split("CORRECTA:")[0]) # Muestra solo la pregunta
    
    opcion = st.radio("Elige tu respuesta:", ["A", "B", "C"], key="respuesta_usuario")
    
    if st.button("Verificar respuesta"):
        respuesta_correcta = st.session_state.quiz_data.split("CORRECTA:")[1].strip()[0]
        if opcion == respuesta_correcta:
            st.success("¡Excelente! Es correcto. 🎉")
        else:
            st.error(f"Oh, no. La respuesta correcta era la {respuesta_correcta}. ¡Sigue intentándolo!")
            st.session_state.evaluado = True
