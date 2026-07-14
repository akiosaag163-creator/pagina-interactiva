import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# Función para encontrar un modelo que funcione
def get_model():
    # Listar modelos disponibles
    models = genai.list_models()
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = get_model()
    if model is None:
        st.error("No se encontró ningún modelo compatible en tu cuenta.")
        st.stop()
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
            instruccion = f"Eres un profesor experto. Si el usuario pide una historia, crea una historia interactiva sobre {prompt} con una decisión final. Si pide un quiz, haz 3 preguntas."
            response = model.generate_content(instruccion)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
