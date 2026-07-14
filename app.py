import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")
st.title("🎓 Mentor Estelar: Historias y Desafíos")

# Configuración API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input usuario
if prompt := st.chat_input("Escribe 'Historia de...' o 'Quiz de...'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrucción diferenciada
        if "quiz" in prompt.lower():
            instruccion = f"""Eres un profesor experto. Crea un quiz de 3 preguntas sobre {prompt}. 
            Cada pregunta debe tener 4 opciones (A, B, C, D). 
            Al final, incluye una lista de respuestas correctas oculta o separada."""
        else:
            instruccion = f"""Eres un narrador experto. Crea una historia interactiva fascinante sobre {prompt}.
            La historia debe tener una trama que cambie según la elección. 
            Termina obligatoriamente con dos opciones: [Opción A] y [Opción B]."""
        
        response = model.generate_content(instruccion)
        respuesta_ia = response.text
        st.markdown(respuesta_ia)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})

        # Mostrar botones solo si la IA generó opciones
        if "[Opción A]" in respuesta_ia or "A)" in respuesta_ia:
            col1, col2 = st.columns(2)
            if col1.button("Elegir Opción A"):
                st.info("Has seleccionado la A. Continúa la aventura...")
            if col2.button("Elegir Opción B"):
                st.info("Has seleccionado la B. La historia toma un nuevo rumbo...")
