import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import base64
import os

# ==========================================
# 1. CONFIGURACIÓN DE SEGURIDAD (API KEY)
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]
else:
    GOOGLE_API_KEY = None

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ Configuración incompleta: No se encontró la variable 'GEMINI_API_KEY' en los secretos de Streamlit.")

# ==========================================
# 2. CONFIGURACIÓN DE LA PÁGINA Y DISEÑO CSS
# ==========================================
st.set_page_config(page_title="Voto Informado Colombia", page_icon="🇨🇴", layout="wide")

st.markdown("""
    <style>
    /* Bandera de Colombia con efecto de onda fluido */
    .bandera-contenedor {
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    .bandera {
        width: 140px;
        height: 90px;
        background: linear-gradient(
            to bottom, 
            #FCD116 0%, #FCD116 50%, 
            #003893 50%, #003893 75%, 
            #CE1126 75%, #CE1126 100%
        );
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        border-radius: 4px;
        animation: oleaje 2.5s infinite ease-in-out alternate;
    }
    @keyframes oleaje {
        0% { transform: skewY(-4deg) rotate(-1deg); }
        50% { transform: skewY(0deg) rotate(1deg); }
        100% { transform: skewY(4deg) rotate(-1deg); }
    }
    
    /* Nueva Tarjeta Única HTML para evitar bloques blancos vacíos */
    .tarjeta-candidato-unica {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-top: 4px solid #FCD116;
        border-bottom: 4px solid #CE1126;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        text-align: center;
        font-family: system-ui, -apple-system, sans-serif;
        margin-bottom: 20px;
    }

    /* Contenedor de Imagen Estricto y Centrado */
    .contenedor-rostro {
        width: 100%;
        height: 240px; /* Altura ideal fija */
        overflow: hidden;
        border-radius: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f7f7f7;
    }
    .contenedor-rostro img {
        width: 100%;
        height: 100%;
        object-fit: cover;      /* Ajusta y recorta proporcionalmente sin deformar */
        object-position: center; /* Centra el encuadre en el rostro del candidato */
    }

    /* Tipografías internas de la tarjeta */
    .titulo-candidato {
        color: #003893;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 8px 0 4px 0;
    }
    .partido-candidato {
        color: #222222;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }
    .propuesta-candidato {
        color: #444444;
        font-size: 0.88rem;
        text-align: justify;
        line-height: 1.4;
        margin: 0;
        padding: 0 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INTERFAZ GRÁFICA (FRONTEND)
# ==========================================
st.markdown('<div class="bandera-contenedor"><div class="bandera"></div></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #003893;'>Plataforma de Voto Informado</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.1rem;'>Powered by Gemini | Análisis Neutral de Candidatos</p>", unsafe_allow_html=True)
st.write("---")

st.markdown("<h3 style='color: #003893;'>👥 Candidatos Registrados</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

candidatos = [
    {
        "col": col1,
        "nombre": "Abelardo de la Espriella",
        "partido": "Derecha / Conservador",
        "foto": "abelardo.jpg",
        "propuesta": "Enfoque de seguridad estricta, libre mercado, reducción drástica del gasto público, privatizaciones y defensa de las instituciones tradicionales."
    },
    {
        "col": col2,
        "nombre": "Iván Cepeda",
        "partido": "Pacto Histórico / Izquierda",
        "foto": "cepeda.jpg",
        "propuesta": "Justicia social, reformas estructurales profundas al sistema de salud y pensiones, modelo de paz total, transición ambiental y enfoque en derechos humanos."
    },
    {
        "col": col3,
        "nombre": "Paloma Valencia",
        "partido": "Centro Democrático / Derecha",
        "foto": "paloma.png",
        "propuesta": "Reforma integral a la justicia, incentivos y créditos para el sector agrícola nacional, doctrina de seguridad democrática y oposición firme a las reformas estatales de izquierda."
    },
    {
        "col": col4,
        "nombre": "Sergio Fajardo",
        "partido": "Centro / Dignidad y Compromiso",
        "foto": "fajardo.jpg",
        "propuesta": "La educación y las regiones como motores principales del desarrollo nacional, transparencia absoluta en la contratación pública y fomento de la innovación tecnológica y científica."
    }
]

for cand in candidatos:
    with cand["col"]:
        # Verificamos si la foto existe localmente para codificarla en Base64
        if os.path.exists(cand["foto"]):
            with open(cand["foto"], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            img_html = f'<img src="data:image/jpeg;base64,{encoded_string}">'
        else:
            img_html = f'<div style="color:#777; font-size:0.9rem;">Falta archivo<br><b>{cand["foto"]}</b></div>'
            
        # Renderizamos TODA la tarjeta de manera unificada mediante un único bloque HTML inyectado
        st.markdown(f"""
            <div class="tarjeta-candidato-unica">
                <div class="contenedor-rostro">
                    {img_html}
                </div>
                <div class="titulo-candidato">{cand['nombre']}</div>
                <div class="partido-candidato"><b>Línea/Partido:</b><br>{cand['partido']}</div>
                <p class="propuesta-candidato"><i>Enfoque:</i> {cand['propuesta']}</p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 4. CHAT CON LA IA
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Consulta al Asistente Electoral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Pregúntame sobre Abelardo, Cepeda, Paloma o Fajardo..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if GOOGLE_API_KEY:
        contexto_sistema = (
            f"Eres un chatbot electoral neutral y altamente objetivo para Colombia. "
            f"Analiza de forma equilibrada los perfiles programáticos de estos candidatos sin tomar partido por ninguno:\n"
            f"1. Abelardo de la Espriella: {candidatos[0]['propuesta']}\n"
            f"2. Iván Cepeda: {candidatos[1]['propuesta']}\n"
            f"3. Paloma Valencia: {candidatos[2]['propuesta']}\n"
            f"4. Sergio Fajardo: {candidatos[3]['propuesta']}\n"
            f"Responde la consulta del usuario manteniendo la neutralidad, basándote en sus agendas y promoviendo el voto informado."
        )

        try:
            response = model.generate_content(contexto_sistema + user_prompt)
            bot_response = response.text
            with st.chat_message("assistant"):
                st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        except Exception as e:
            st.error(f"Error en la consulta: {e}")
    else:
        st.warning("El chat no puede responder porque la API Key no está configurada en el servidor.")

# ==========================================
# 5. INTEGRACIÓN DE INTERFAZ HTML (VOTO INFORMADO 2.0)
# ==========================================
st.write("---")
st.markdown("<h3 style='color: #003893;'>📊 Test de Afinidad y Matriz Programática</h3>", unsafe_allow_html=True)

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_source = f.read()
    components.html(html_source, height=1100, scrolling=True)
else:
    st.error("❌ Archivo 'index.html' no encontrado en el repositorio.")