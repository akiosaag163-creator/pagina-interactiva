import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# Configuración usando el nombre exacto de tu lista
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos el nombre exacto que confirmó tu diagnóstico
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu tema de ciencia..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Instrucción clara
            instruccion = f"Eres un profesor experto. Si el usuario pide una historia, crea una historia interactiva sobre {prompt} con una decisión final. Si pide un quiz, haz 3 preguntas."
            response = model.generate_content(instruccion)
            full_text = response.text
            message_placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
