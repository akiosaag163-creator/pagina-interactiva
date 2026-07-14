import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Chatbot de Ciencia", page_icon="🧪")

# Configuración de la IA desde los Secrets de Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

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
        instruccion = f"Eres un profesor de ciencias. Crea una historia interactiva sobre {prompt} con una decisión al final."
        response = model.generate_content(instruccion)
        full_response = response.text
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
