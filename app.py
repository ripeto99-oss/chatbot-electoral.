import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os

# ==========================================
# 1. CONFIGURACIÓN DE SEGURIDAD (API KEY)
# ==========================================
# El código buscará la clave en los secretos del servidor o de Streamlit
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
    
    /* Tarjetas de los Candidatos */
    .candidato-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-top: 4px solid #FCD116;
        border-bottom: 4px solid #CE1126;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s;
        min-height: 520px;
    }
    .candidato-card:hover {
        transform: translateY(-5px);
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

# Mapeo estricto con las extensiones exactas de tus archivos locales
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
        st.markdown('<div class="candidato-card">', unsafe_allow_html=True)
        
        # Validación de archivos locales en el repositorio para evitar imágenes rotas
        if os.path.exists(cand["foto"]):
            st.image(cand["foto"], use_container_width=True)
        else:
            st.warning(f"Falta subir '{cand['foto']}' a GitHub")
            
        st.markdown(f"<h4 style='color: #003893; margin-top: 10px;'>{cand['nombre']}</h4>", unsafe_allow_html=True)
        st.markdown(f"**Línea/Partido:**<br>{cand['partido']}", unsafe_allow_html=True)
        st.markdown(f"*Enfoque:* {cand['propuesta']}")
        st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Despliega de forma nativa tu HTML con gráficos y modales funcionales
    components.html(html_source, height=1100, scrolling=True)
else:
    st.error("❌ Archivo 'index.html' no encontrado en el repositorio.")