import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓", layout="centered")

st.title("🎓 ¡Bienvenido a Mentor Estelar! 🚀")

# Configuración de la API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error("Configuración de API no encontrada. Revisa tus Secrets.")
    st.stop()

# Inicializar estados
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué quieres aprender hoy? (ej: 'Historia de la fotosíntesis' o 'Quiz de biología')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('El mentor está preparando tu lección...'):
            # Lógica diferenciada por tipo de solicitud
            if "quiz" in prompt.lower():
                instruccion = f"Eres un profesor experto. Haz 3 preguntas de evaluación directa (sin opciones) sobre: {prompt}. No incluyas historias, solo las preguntas."
            else:
                instruccion = f"""Eres un profesor experto. Crea una historia interactiva sobre {prompt}. 
                Al final, presenta dos opciones claras etiquetadas como:
                [Opción A] y [Opción B]."""
            
            response = model.generate_content(instruccion)
            full_text = response.text
            st.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            
            # Botones para historias interactivas
            if "historia" in prompt.lower() or ("Opción A" in full_text and "Opción B" in full_text):
                col1, col2 = st.columns(2)
                if col1.button("Elegir Opción A"):
                    st.write("Has elegido la Opción A. ¡El mentor procesará tu elección en la siguiente pregunta!")
                if col2.button("Elegir Opción B"):
                    st.write("Has elegido la Opción B. ¡El mentor procesará tu elección en la siguiente pregunta!")
