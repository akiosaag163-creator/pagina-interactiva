import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# 1. Configurar conexión
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# 2. Manejo de estado del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input y respuesta
if prompt := st.chat_input("Escribe tu tema:"):
    # Mostrar usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Crea un espacio vacío para la respuesta
        try:
            full_text = ""
            # Pedimos la respuesta
            response = model.generate_content(f"Eres un profesor de ciencias. Responde brevemente a: {prompt}")
            full_text = response.text
            
            message_placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"Error al generar: {e}")
