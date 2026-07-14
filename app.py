import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")

# Estilos CSS para el fondo morado y diseño profesional
st.markdown("""
    <style>
    .stApp { background-color: #2e003e; color: white; }
    h1, h2, h3 { color: #d1c4e9; }
    .stButton>button { border-radius: 20px; background-color: #7b1fa2; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Mentor Estelar: Camino al Saber")

# Configuración API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
else:
    st.error("Configura tu API KEY en Secrets.")
    st.stop()

# Inicializar estados de progreso
if "xp" not in st.session_state: st.session_state.xp = 0
if "history" not in st.session_state: st.session_state.history = []

# Barra lateral de progreso
st.sidebar.header("📈 Tu Progreso")
nivel = st.session_state.xp // 50
st.sidebar.write(f"Nivel: {nivel}")
st.sidebar.progress(min((st.session_state.xp % 50) / 50, 1.0))

# Mostrar Chat
for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# Input del usuario
if prompt := st.chat_input("Pide un 'Quiz de...' o 'Historia de...'"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner('El mentor está calculando...'):
            try:
                # Instrucción optimizada
                es_quiz = "quiz" in prompt.lower()
                instruccion = f"Crea un {('quiz de 3 preguntas (A, B, C, D) con respuestas') if es_quiz else 'historia interactiva con [Opción A] y [Opción B]'} sobre {prompt}."
                
                resp = model.generate_content(instruccion)
                texto = resp.text
                st.markdown(texto)
                st.session_state.history.append({"role": "assistant", "content": texto})
                
                # Sistema de puntos al generar contenido
                st.session_state.xp += 10
                st.rerun()
            except Exception as e:
                st.warning("El mentor está descansando (Límite de API). Intenta en un momento.")

# Botones interactivos (Solo si aparecen en el texto)
last_msg = st.session_state.history[-1]["content"] if st.session_state.history else ""
if "[Opción A]" in last_msg or "Opción A" in last_msg:
    col1, col2 = st.columns(2)
    if col1.button("Elegir Opción A"): st.success("¡Bien! Ganaste +5 XP.")
    if col2.button("Elegir Opción B"): st.success("¡Interesante elección! Ganaste +5 XP.")
