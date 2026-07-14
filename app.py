import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")
st.title("🎓 Mentor Estelar: Ciencias y Matemáticas")

# Configuración API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
else:
    st.error("Por favor configura tu GEMINI_API_KEY en los Secrets.")
    st.stop()

# Inicialización de estado
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None

# Input del usuario
prompt = st.chat_input("¿Qué quieres hoy? (Ej: 'Historia de la gravedad' o 'Quiz de álgebra')")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('El mentor está preparando tu desafío...'):
            if "quiz" in prompt.lower():
                instruccion = f"""Eres un profesor de ciencias/mates. Crea una pregunta de quiz sobre {prompt}.
                Formato obligatorio:
                PREGUNTA: [La pregunta]
                A) [Opción]
                B) [Opción]
                C) [Opción]
                CORRECTA: [Letra]"""
                response = model.generate_content(instruccion)
                st.session_state.quiz_data = response.text
                st.markdown(response.text.split("CORRECTA:")[0])
            else:
                instruccion = f"""Eres un narrador científico. Crea una historia interactiva corta sobre {prompt}.
                Termina obligatoriamente con:
                [Opción A] Final alternativo 1
                [Opción B] Final alternativo 2"""
                response = model.generate_content(instruccion)
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# Lógica de resolución (Botones)
if st.session_state.quiz_data:
    st.markdown("---")
    opcion = st.radio("Elige tu respuesta:", ["A", "B", "C"], key="r")
    if st.button("Verificar Quiz"):
        correcta = st.session_state.quiz_data.split("CORRECTA:")[1].strip()[0]
        if opcion == correcta:
            st.success("¡Excelente, correcto! 🎉")
        else:
            st.error(f"Incorrecto. La respuesta era {correcta}.")

if any("[Opción A]" in msg.get("content", "") for msg in st.session_state.chat_history):
    col1, col2 = st.columns(2)
    if col1.button("Elegir Opción A"): st.info("Has cambiado el destino de la historia...")
    if col2.button("Elegir Opción B"): st.info("La historia ha tomado otro camino...")
