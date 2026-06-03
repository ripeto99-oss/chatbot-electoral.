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
# 2. CONFIGURACION
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")
SYSTEM_INSTRUCTION = (
    "Eres un analista electoral neutral para Colombia. Tu objetivo es responder consultas "
    "de forma totalmente objetiva y sin sesgos politicos. Utiliza unicamente datos programaticos "
    "reales para explicar el panorama de manera educativa y equilibrada."
)

# ==========================================
# 3. FUNCIONES
# ==========================================
@st.cache_data(show_spinner=False)
def cargar_imagen_base64(ruta_foto):
    if os.path.exists(ruta_foto):
        with open(ruta_foto, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# ==========================================
# 4. ESTILOS CSS
# ==========================================
st.markdown("""
    <style>
    .bandera-contenedor { display: flex; justify-content: center; margin-bottom: 25px; }
    .bandera { width: 140px; height: 90px; background: linear-gradient(to bottom, #FCD116 50%, #003893 25%, #CE1126 25%); border-radius: 4px; box-shadow: 0px 5px 15px rgba(0,0,0,0.3); }
    .tarjeta-candidato-unica { background-color: #ffffff; padding: 15px; border-radius: 12px; border-top: 4px solid #FCD116; border-bottom: 4px solid #CE1126; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); text-align: center; margin-bottom: 20px; min-height: 565px; display: flex; flex-direction: column; }
    .contenedor-rostro { width: 100%; height: 240px; overflow: hidden; border-radius: 8px; margin-bottom: 12px; }
    .contenedor-rostro img { width: 100%; height: 100%; object-fit: cover; }
    .titulo-candidato { color: #003893; font-size: 1.2rem; font-weight: bold; margin: 8px 0 4px 0; }
    .propuesta-candidato { color: #444444; font-size: 0.88rem; text-align: justify; line-height: 1.4; padding: 0 5px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. UI PRINCIPAL
# ==========================================
st.markdown('<div class="bandera-contenedor"><div class="bandera"></div></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #003893;'>Plataforma de Voto Informado</h1>", unsafe_allow_html=True)

candidatos = [
    {"nombre": "Abelardo de la Espriella", "partido": "Derecha", "foto": "abelardo.jpg", "propuesta": "Enfoque de seguridad estricta, libre mercado, reducción drástica del gasto público y defensa de instituciones tradicionales."},
    {"nombre": "Ivan Cepeda", "partido": "Izquierda", "foto": "cepeda.jpg", "propuesta": "Justicia social, reformas estructurales profundas al sistema de salud y pensiones, modelo de paz total y enfoque en derechos humanos."},
    {"nombre": "Paloma Valencia", "partido": "Derecha", "foto": "paloma.png", "propuesta": "Reforma integral a la justicia, incentivos al sector agrícola nacional, doctrina de seguridad democrática y oposición firme a reformas de izquierda."},
    {"nombre": "Sergio Fajardo", "partido": "Centro", "foto": "fajardo.jpg", "propuesta": "La educación y las regiones como motores del desarrollo nacional, transparencia en contratación pública y fomento de innovación tecnológica."}
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
                <p><b>Linea:</b> {cand['partido']}</p>
                <p class="propuesta-candidato"><i>Enfoque:</i> {cand['propuesta']}</p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 6. CHAT Y HTML FINAL
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Asistente Electoral</h3>", unsafe_allow_html=True)
if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages: st.chat_message(m["role"]).markdown(m["content"])

if user_prompt := st.chat_input("Preguntame sobre los candidatos..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    if GOOGLE_API_KEY:
        with st.chat_message("assistant"):
            try:
                p_final = f"{SYSTEM_INSTRUCTION}\n\nPregunta: {user_prompt}"
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                r = requests.post(url, json={"contents": [{"parts": [{"text": p_final}]}]})
                if r.status_code == 200:
                    resp = r.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(resp)
                    st.session_state.messages.append({"role": "assistant", "content": resp})
            except Exception as e: st.error(f"Error: {e}")

components.html("""<div style="background-color: #1e293b; padding: 40px; border-radius: 12px; text-align: center; color: white;">
    <h2 style="color: #FCD116;">¿Quien merece tu voto en la Colombia de 2026?</h2>
    <p>Analiza los planes de gobierno reales de forma objetiva.</p>
    <div style="background-color: #003893; padding: 12px; border-radius: 6px; font-weight: bold;">Iniciar Test</div>
</div>""", height=300)
