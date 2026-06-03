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
# 2. CONFIGURACION DE LLAVE Y SISTEMA
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")
SYSTEM_INSTRUCTION = (
    "Eres un analista electoral neutral para Colombia. Tu objetivo es responder consultas "
    "de forma totalmente objetiva y sin sesgos politicos. Utiliza unicamente datos programaticos "
    "reales para explicar el panorama de manera educativa y equilibrada."
)

# ==========================================
# 3. FUNCIONES Y ESTILOS
# ==========================================
@st.cache_data(show_spinner=False)
def cargar_imagen_base64(ruta_foto):
    if os.path.exists(ruta_foto):
        with open(ruta_foto, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

st.markdown("""
    <style>
    .bandera-contenedor { display: flex; justify-content: center; margin-bottom: 25px; }
    .bandera { width: 140px; height: 90px; background: linear-gradient(to bottom, #FCD116 50%, #003893 25%, #CE1126 25%); border-radius: 4px; }
    .tarjeta-candidato-unica { background-color: #ffffff; padding: 15px; border-radius: 12px; border-top: 4px solid #FCD116; border-bottom: 4px solid #CE1126; box-shadow: 0 4px 8px rgba(0,0,0,0.15); text-align: center; margin-bottom: 20px; min-height: 500px; }
    .contenedor-rostro { width: 100%; height: 200px; overflow: hidden; border-radius: 8px; margin-bottom: 12px; }
    .contenedor-rostro img { width: 100%; height: 100%; object-fit: cover; }
    .titulo-candidato { color: #003893; font-size: 1.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. INTERFAZ (TARJETAS)
# ==========================================
st.markdown('<div class="bandera-contenedor"><div class="bandera"></div></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #003893;'>Plataforma de Voto Informado</h1>", unsafe_allow_html=True)

candidatos = [
    {"nombre": "Abelardo de la Espriella", "partido": "Derecha", "foto": "abelardo.jpg", "propuesta": "Seguridad estricta y mercado."},
    {"nombre": "Ivan Cepeda", "partido": "Izquierda", "foto": "cepeda.jpg", "propuesta": "Justicia social y paz."},
    {"nombre": "Paloma Valencia", "partido": "Derecha", "foto": "paloma.png", "propuesta": "Reforma justicia y agro."},
    {"nombre": "Sergio Fajardo", "partido": "Centro", "foto": "fajardo.jpg", "propuesta": "Educación y regiones."}
]

cols = st.columns(4)
for i, cand in enumerate(candidatos):
    with cols[i]:
        string_base64 = cargar_imagen_base64(cand["foto"])
        img_html = f'<img src="data:image/jpeg;base64,{string_base64}">' if string_base64 else "Sin foto"
        st.markdown(f"""
            <div class="tarjeta-candidato-unica">
                <div class="contenedor-rostro">{img_html}</div>
                <div class="titulo-candidato">{cand['nombre']}</div>
                <p>{cand['partido']}</p>
                <p><i>{cand['propuesta']}</i></p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 5. CHAT (CONEXIÓN SEGURA)
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Asistente Electoral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

user_prompt = st.chat_input("Preguntame sobre los candidatos...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    if GOOGLE_API_KEY:
        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                prompt_final = f"{SYSTEM_INSTRUCTION}\n\nPregunta: {user_prompt}"
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                payload = {"contents": [{"parts": [{"text": prompt_final}]}]}
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        bot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        st.error(f"Error {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# 6. COMPONENTE HTML PERSONALIZADO (Lo que faltaba)
# ==========================================
st.write("---")
st.markdown("<h3 style='color: #003893;'>📊 Test de Afinidad y Matriz Programática</h3>", unsafe_allow_html=True)

html_seguro = """
<div style="background-color: #1e293b; padding: 40px; border-radius: 12px; text-align: center; font-family: sans-serif; color: white;">
    <h2 style="color: #FCD116; margin-bottom: 10px;">¿Quien merece tu voto en la Colombia de 2026?</h2>
    <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 600px; margin: 0 auto 25px auto;">
        Analiza los planes de gobierno reales de los candidatos presidenciales mediante datos estructurados y modelos algoritmicos objetivos.
    </p>
    <div style="display: inline-block; background-color: #003893; color: white; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer;">
        Iniciar Test de Afinidad
    </div>
</div>
"""

components.html(html_seguro, height=300, scrolling=False)
