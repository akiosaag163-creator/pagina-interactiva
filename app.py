import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# Configuración
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu tema:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrucción para que dé opciones con formato claro
        instruccion = f"""Eres un profesor experto. Crea una historia corta o quiz sobre {prompt}.
        Si es historia, termina con dos opciones etiquetadas como [Opción A] y [Opción B]."""
        
        response = model.generate_content(instruccion)
        full_text = response.text
        st.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})
        
        # Lógica para botones si el bot propuso opciones
        if "[Opción A]" in full_text and "[Opción B]" in full_text:
            col1, col2 = st.columns(2)
            if col1.button("Elegir Opción A"):
                st.write("Has elegido la opción A. ¡Vamos allá!")
            if col2.button("Elegir Opción B"):
                st.write("Has elegido la opción B. ¡Continuemos!")
