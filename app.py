import streamlit as st
import google.generativeai as genai

# 1. Configuración inicial
st.set_page_config(page_title="Mentor Científico", page_icon="🎓")
st.title("🎓 Mentor de Ciencias y Matemáticas")

# 2. Configurar la IA
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Error: Configura tu GEMINI_API_KEY en los Secrets.")
    st.stop()

# 3. Mantener el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar el historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Caja de texto para escribir
if prompt := st.chat_input("Escribe tu tema de ciencia o pide un quiz..."):
    # Guardar y mostrar lo que escribiste
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generar respuesta
    with st.chat_message("assistant"):
        instruccion = f"Eres un profesor experto. Si el usuario pide una historia, crea una historia interactiva sobre {prompt} con una decisión final. Si el usuario pide un quiz o examen, genera 3 preguntas de opción múltiple sobre {prompt}."
        
        try:
            response = model.generate_content(instruccion)
            full_response = response.text
            st.markdown(full_response)
            # Guardar la respuesta de la IA
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error("Hubo un error al generar la respuesta. Intenta de nuevo.")
