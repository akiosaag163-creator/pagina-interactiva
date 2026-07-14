import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

try:
    # Configuración con el modelo nuevo y correcto
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # USAMOS GEMINI-1.5-FLASH
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
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
            instruccion = f"Eres un profesor experto. Crea una historia interactiva sobre {prompt} o un quiz de 3 preguntas si el usuario lo pide."
            response = model.generate_content(instruccion)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
