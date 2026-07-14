import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Mentor Estelar 🚀", page_icon="🎓")
st.title("🎓 Mentor Estelar: Aprende y Juega")

# Configuración
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
except:
    st.error("Error de configuración.")
    st.stop()

if "history" not in st.session_state: st.session_state.history = []

# Mostrar chat
for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# Input
if prompt := st.chat_input("Pide un 'Quiz de...' o 'Historia de...'"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner('El mentor está preparando tu desafío...'):
            try:
                # Instrucción directa
                modo = "quiz de 3 preguntas con opciones A, B, C, D" if "quiz" in prompt.lower() else "historia interactiva con opciones [Opción A] y [Opción B]"
                resp = model.generate_content(f"Crea un {modo} sobre {prompt}")
                texto = resp.text
                st.markdown(texto)
                st.session_state.history.append({"role": "assistant", "content": texto})
                
                # Renderizar botones basados en lo que devolvió la IA
                if "[Opción A]" in texto or "Opción A" in texto:
                    col1, col2 = st.columns(2)
                    if col1.button("Elegir Opción A"): st.success("Elegiste A. El mentor continuará la historia...")
                    if col2.button("Elegir Opción B"): st.success("Elegiste B. El mentor continuará la historia...")
                
                elif "A)" in texto or "A." in texto:
                    opcion = st.radio("Selecciona tu respuesta:", ["A", "B", "C", "D"], key="quiz_sel")
                    if st.button("Verificar respuesta"):
                        st.info(f"Has seleccionado {opcion}. (El mentor evaluará tu elección en el próximo mensaje).")

            except Exception as e:
                st.warning("El mentor está tomando un breve descanso. Por favor, espera 30 segundos y vuelve a intentar.")
