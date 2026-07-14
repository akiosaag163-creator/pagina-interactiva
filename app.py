import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Científico", page_icon="🎓")

# Configuración de la IA
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Error: Configura tu GEMINI_API_KEY en los Secrets.")
    st.stop()

st.title("🎓 Mentor de Ciencias y Matemáticas")
st.write("Dime qué quieres: una **historia interactiva** (Biología, Ciencias) o un **Quiz** (Mates, Física, Química).")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ejemplo: 'Hazme un quiz de física' o 'Historia de biología'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrucción inteligente para diferenciar entre historia y quiz
        instruccion = f"""
        Actúa como un profesor experto. Si el usuario pide una historia, crea una historia interactiva 
        sobre {prompt} con una decisión final. 
        Si el usuario pide un quiz o examen, genera 3 preguntas de opción múltiple sobre {prompt}, 
        espera a que el usuario responda, y luego corrige sus respuestas.
        """
        
        try:
            response = model.generate_content(instruccion)
            full_response = response.text
            st.markdown(full_response)
        except Exception as e:
            full_response = "Error al generar el contenido. Intenta de nuevo."
            st.error(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
