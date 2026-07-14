import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓", layout="wide")

# Estilos CSS para hacerlo más "llamativo"
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #f0f2f6, #e1f5fe); }
    .css-1r6slb0 { font-weight: bold; color: #1e88e5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 ¡Bienvenido a Mentor Estelar! 🚀")
st.subheader("Tu guía inteligente hacia el conocimiento infinito")

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.xp = 0 # Nivel de experiencia

# Sidebar para motivación
with st.sidebar:
    st.header("🌟 Tu Progreso")
    st.progress(min(st.session_state.xp / 100, 1.0))
    st.write(f"Nivel actual: **{int(st.session_state.xp/10)}**")
    st.info("¡Cada pregunta te hace más sabio! Sigue aprendiendo.")

# Interfaz principal
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"], use_container_width=True)

if prompt := st.chat_input("¿Qué maravilla científica quieres descubrir hoy?"):
    st.session_state.xp += 10 # Ganar XP por preguntar
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('El mentor está procesando tu sabiduría...'):
            instruccion = f"""Eres un mentor científico entusiasta y motivador. 
            Crea una explicación breve o historia sobre: {prompt}.
            Incluye al final una pregunta para que el usuario demuestre lo aprendido.
            IMPORTANTE: Termina tu respuesta con 'IMAGE_URL: https://source.unsplash.com/800x400/?{prompt.replace(' ', '+')}'"""
            
            response = model.generate_content(instruccion)
            full_text = response.text
            
            # Limpiar imagen
            text_content = full_text.split("IMAGE_URL:")[0]
            image_url = full_text.split("IMAGE_URL:")[1].strip() if "IMAGE_URL:" in full_text else None
            
            st.markdown(text_content)
            if image_url:
                st.image(image_url, caption="Tu ilustración científica", use_container_width=True)
            
            st.session_state.messages.append({"role": "assistant", "content": text_content, "image_url": image_url})
            st.rerun() # Recargar para actualizar la barra de progreso
