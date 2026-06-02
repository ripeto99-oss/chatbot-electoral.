import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import base64
import os

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (DEBE IR PRIMERO)
# ==========================================
st.set_page_config(page_title="Voto Informado Colombia", page_icon="🇨🇴", layout="wide")

# ==========================================
# 2. CONFIGURACIÓN DE SEGURIDAD (API KEY)
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]
else:
    GOOGLE_API_KEY = None

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error al inicializar Gemini: {e}")
else:
    st.error("⚠️ Configuración incompleta: No se encontró la variable 'GEMINI_API_KEY' en los secretos.")

# ==========================================
# 3. CACHÉ DE IMÁGENES (Optimización de memoria)
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
# 4. DISEÑO CSS PERSONALIZADO
# ==========================================
st.markdown("""
    <style>
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
    }
    
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
        min-height: 565px;
        display: flex;
        flex-direction: column;
    }

    .contenedor-rostro {
        width: 100%;
        height: 240px; 
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
        object-fit: cover;
    }

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
        min-height: 40px;
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
# 5. INTERFAZ GRÁFICA (TARJETAS)
# ==========================================
st.markdown('<div class="bandera-contenedor"><div class="bandera"></div></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #003893;'>Plataforma de Voto Informado</h1>", unsafe_allow_html=True)
st.write("---")

st.markdown("<h3 style='color: #003893;'>👥 Candidatos Registrados</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

candidatos = [
    {
        "col": col1, "nombre": "Abelardo de la Espriella", "partido": "Derecha / Conservador", "foto": "abelardo.jpg",
        "css_custom": "object-position: center 15%; transform: scale(1.05);",
        "propuesta": "Enfoque de seguridad estricta, libre mercado, reducción drástica del gasto público, privatizaciones y defensa de las instituciones tradicionales."
    },
    {
        "col": col2, "nombre": "Iván Cepeda", "partido": "Pacto Histórico / Izquierda", "foto": "cepeda.jpg",
        "css_custom": "object-position: center 38%; transform: scale(1.1);", 
        "propuesta": "Justicia social, reformas estructurales profundas al sistema de salud y pensiones, modelo de paz total, transición ambiental y enfoque en derechos humanos."
    },
    {
        "col": col3, "nombre": "Paloma Valencia", "partido": "Centro Democrático / Derecha", "foto": "paloma.png",
        "css_custom": "object-position: center 15%; transform: scale(0.9);",
        "propuesta": "Reforma integral a la justicia, incentivos y créditos para el sector agrícola nacional, doctrina de seguridad democrática y oposición firme a las reformas estatales de izquierda."
    },
    {
        "col": col4, "nombre": "Sergio Fajardo", "partido": "Centro / Dignidad y Compromiso", "foto": "fajardo.jpg",
        "css_custom": "object-position: center 25%; transform: scale(1.05);",
        "propuesta": "La educación y las regiones como motores principales del desarrollo nacional, transparencia absoluta en la contratación pública y fomento de la innovación tecnológica y científica."
    }
]

for cand in candidatos:
    with cand["col"]:
        string_base64 = cargar_imagen_base64(cand["foto"])
        if string_base64:
            img_html = f'<img src="data:image/jpeg;base64,{string_base64}" style="{cand["css_custom"]}">'
        else:
            img_html = f'<div style="color:#777; font-size:0.9rem;">Falta foto<br><b>{cand["foto"]}</b></div>'
            
        st.markdown(f"""
            <div class="tarjeta-candidato-unica">
                <div class="contenedor-rostro">{img_html}</div>
                <div class="titulo-candidato">{cand['nombre']}</div>
                <div class="partido-candidato"><b>Línea/Partido:</b><br>{cand['partido']}</div>
                <p class="propuesta-candidato"><i>Enfoque:</i> {cand['propuesta']}</p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 6. SISTEMA DE CHAT REFORZADO (ANTI-CONGELAMIENTO)
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Consulta al Asistente Electoral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderizar historial guardado
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar entrada del usuario de forma aislada
if user_prompt := st.chat_input("Pregúntame sobre Abelardo, Cepeda, Paloma o Fajardo..."):
    # Mostrar inmediatamente en pantalla el texto del usuario
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Ejecutar la llamada a la IA de manera controlada con una barra de carga temporal
    if GOOGLE_API_KEY:
        contexto_sistema = (
            f"Eres un chatbot electoral neutral y altamente objetivo para Colombia. "
            f"Analiza de forma equilibrada los perfiles programáticos de estos candidatos sin tomar partido por ninguno:\n"
            f"1. Abelardo de la Espriella: {candidatos[0]['propuesta']}\n"
            f"2. Iván Cepeda: {candidatos[1]['propuesta']}\n"
            f"3. Paloma Valencia: {candidatos[2]['propuesta']}\n"
            f"4. Sergio Fajardo: {candidatos[3]['propuesta']}\n"
            f"Responde la consulta de manera concreta, neutral y basándote en sus propuestas reales."
        )
        
        with st.spinner("Pensando respuesta neutral..."):
            try:
                response = model.generate_content(contexto_sistema + "\nUsuario: " + user_prompt)
                bot_response = response.text
                
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.rerun() # Fuerza la actualización de la interfaz de forma limpia
            except Exception as e:
                st.error(f"La API de Gemini tardó demasiado o falló: {e}")
    else:
        st.warning("Falta la API Key para procesar tu consulta.")

# ==========================================
# 7. COMPONENTE HTML EXTERNO (AL FINAL)
# ==========================================
st.write("---")
st.markdown("<h3 style='color: #003893;'>📊 Test de Afinidad y Matriz Programática</h3>", unsafe_allow_html=True)

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_source = f.read()
    # Ejecución aislada dentro de un iframe controlado para evitar que rompa el loop de Streamlit
    components.html(html_source, height=900, scrolling=True)
else:
    st.error("❌ Archivo 'index.html' no encontrado.")