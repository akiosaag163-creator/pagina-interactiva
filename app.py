import streamlit as st
import google.generativeai as genai

# 1. Configuración de página y Estilos CSS (Tema Morado Astral)
st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")
st.markdown("""
    <style>
    .stApp { background-color: #2e003e; color: #ffffff; }
    h1, h2, h3 { color: #d1c4e9; }
    .stButton>button { border-radius: 20px; background-color: #7b1fa2; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Configuración API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
except:
    st.error("Error: Configura tu GEMINI_API_KEY en los secretos.")
    st.stop()

# 3. Inicialización de Estado (Progreso y Registro)
if "user_name" not in st.session_state: st.session_state.user_name = None
if "xp" not in st.session_state: st.session_state.xp = 0
if "history" not in st.session_state: st.session_state.history = []

# Registro de Usuario
if not st.session_state.user_name:
    st.title("🎓 Bienvenido al Mentor Estelar")
    name = st.text_input("Ingresa tu nombre de viajero astral:")
    if st.button("Comenzar Viaje"):
        st.session_state.user_name = name
        st.rerun()
    st.stop()

# Barra Lateral de Progreso
st.sidebar.header(f"✨ Viajero: {st.session_state.user_name}")
st.sidebar.write(f"Nivel: {st.session_state.xp // 50}")
st.sidebar.progress(min((st.session_state.xp % 50) / 50, 1.0))

st.title("🎓 Mentor Estelar: Ciencias y Mates")

# Chat
for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# Input del Usuario
if prompt := st.chat_input("¿Qué deseas explorar? (Ej: 'Quiz de física' o 'Historia de los números')"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner('El mentor está preparando tu desafío...'):
            try:
                es_quiz = "quiz" in prompt.lower()
                modo = "un quiz de 3 preguntas con opciones A, B, C, D" if es_quiz else "una historia interactiva con opciones [Opción A] y [Opción B]"
                resp = model.generate_content(f"Crea {modo} sobre {prompt}.")
                texto = resp.text
                st.markdown(texto)
                st.session_state.history.append({"role": "assistant", "content": texto})
                
                st.session_state.xp += 10
                st.rerun()
            except Exception as e:
                st.warning("El mentor está descansando un momento (Límite API). Espera unos segundos.")

# Botones de Interacción
last_msg = st.session_state.history[-1]["content"] if st.session_state.history else ""
if "[Opción A]" in last_msg or "Opción A" in last_msg:
    col1, col2 = st.columns(2)
    if col1.button("Elegir Opción A"): 
        st.success("¡Excelente elección! +5 XP")
        st.session_state.xp += 5
    if col2.button("Elegir Opción B"): 
        st.success("¡Un rumbo inesperado! +5 XP")
        st.session_state.xp += 5
elif "A)" in last_msg or "A." in last_msg:
    opcion = st.radio("Selecciona tu respuesta:", ["A", "B", "C", "D"], key="quiz")
    if st.button("Verificar"):
        st.info(f"Has marcado {opcion}. ¡Sigue acumulando conocimiento!")
        st.session_state.xp += 5
