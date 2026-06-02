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
col1, col2, col3 = st.columns(3)

candidatos = [
    {
        "col": col1,
        "nombre": "Carlos Mendoza",
        "partido": "Movimiento Avanza Colombia",
        "foto": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400",
        "propuesta": "Transformación digital en colegios públicos y conectividad 5G rural."
    },
    {
        "col": col2,
        "nombre": "Diana Sotomayor",
        "partido": "Coalición Verde y Sostenible",
        "foto": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400",
        "propuesta": "Transición energética justa, protección de páramos y transporte eléctrico."
    },
    {
        "col": col3,
        "nombre": "Alejandro Restrepo",
        "partido": "Frente por el Desarrollo",
        "foto": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400",
        "propuesta": "Reducción de impuestos a PYMES y fortalecimiento de la seguridad urbana."
    }
]

for cand in candidatos:
    with cand["col"]:
        st.markdown('<div class="candidato-card">', unsafe_allow_html=True)
        st.image(cand["foto"], width=180, caption=cand["nombre"])
        st.markdown(f"**Partido:** {cand['partido']}")
        st.markdown(f"*Propuesta:* {cand['propuesta']}")
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

if user_prompt := st.chat_input("Pregúntame sobre los candidatos o contrasta sus propuestas..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if GOOGLE_API_KEY:
        contexto_sistema = (
            f"Eres un chatbot electoral neutral para Colombia. "
            f"Candidatos:\n"
            f"1. Carlos Mendoza: {candidatos[0]['propuesta']}\n"
            f"2. Diana Sotomayor: {candidatos[1]['propuesta']}\n"
            f"3. Alejandro Restrepo: {candidatos[2]['propuesta']}\n"
            f"Responde con base en estos datos de forma objetiva: "
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

# Comprobamos que el archivo renombrado en tu GitHub realmente exista en el directorio raíz
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_source = f.read()
    
    # Renderizamos tu HTML interactivo con gráficos, modales y estilos nativos
    components.html(html_source, height=1000, scrolling=True)
else:
    st.error("❌ Archivo 'index.html' no encontrado en el repositorio. Verifica el nombre.")