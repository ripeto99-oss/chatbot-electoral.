import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import os

# ==========================================
# 1. CONFIGURACION DE LA PAGINA
# ==========================================
st.set_page_config(page_title="Voto Informado Colombia", page_icon="🇨🇴", layout="wide")

# ==========================================
# 2. CONFIGURACION DE LLAVE (Desde Secrets)
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = (
    "Eres un analista electoral neutral para Colombia. Tu objetivo es responder consultas "
    "de forma totalmente objetiva y sin sesgos politicos. Utiliza unicamente datos programaticos "
    "reales para explicar el panorama de manera educativa y equilibrada."
)

# ==========================================
# 3. FUNCIONES AUXILIARES
# ==========================================
@st.cache_data(show_spinner=False)
def cargar_imagen_base64(ruta_foto):
    if os.path.exists(ruta_foto):
        try:
            with open(ruta_foto, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except Exception:
            return None
    return None

# ==========================================
# 4. CSS Y UI
# ==========================================
st.markdown("""
    <style>
    .bandera-contenedor { display: flex; justify-content: center; margin-bottom: 25px; }
    .bandera { width: 140px; height: 90px; background: linear-gradient(to bottom, #FCD116 50%, #003893 25%, #CE1126 25%); border-radius: 4px; }
    .tarjeta { background-color: #ffffff; padding: 15px; border-radius: 12px; border-top: 4px solid #FCD116; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #003893;'>Plataforma de Voto Informado</h1>", unsafe_allow_html=True)

# ==========================================
# 5. LOGICA DEL CHAT (REST API - V1)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Preguntame sobre los candidatos...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if GOOGLE_API_KEY:
        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                try:
                    # Usamos V1 que es la estable para proyectos de 2026
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                    
                    payload = {
                        "contents": [{"parts": [{"text": user_prompt}]}],
                        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]}
                    }
                    
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        bot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Error crítico: {e}")
    else:
        st.warning("Configura tu API Key en los Secrets.")
