import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# Usaremos un modelo optimizado para velocidad
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu tema:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción directa para velocidad
            instruccion = f"Eres un profesor. Crea una historia interactiva corta o un quiz de 3 preguntas sobre: {prompt}"
            response = model.generate_content(instruccion)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error al generar respuesta. Intenta de nuevo.")
