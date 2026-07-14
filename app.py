
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# Configurar la IA buscando el modelo disponible
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Esta parte busca un modelo que funcione en tu cuenta
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Intentamos usar 'gemini-1.5-flash' o el primero que aparezca en la lista
    model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
    model = genai.GenerativeModel(model_name)
    
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
