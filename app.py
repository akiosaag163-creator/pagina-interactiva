import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página
st.set_page_config(page_title="Chatbot de Ciencia", page_icon="🧪")

# Cargar la API KEY desde los Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("No se encontró la API KEY en los Secrets. Por favor revísalos.")
    st.stop()

st.title("🧪 Chatbot de Ciencias Interactivas")
st.write("Escribe un tema de ciencias y vive una aventura.")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué tema científico quieres explorar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruccion = f"Eres un profesor de ciencias divertido. Crea una historia interactiva corta sobre: {prompt}. Presenta un conflicto científico y al final haz una pregunta de decisión para el usuario."
        try:
            response = model.generate_content(instruccion)
            full_response = response.text
            st.markdown(full_response)
        except Exception as e:
            st.error("Hubo un error al generar la respuesta. Revisa tu API KEY.")
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
