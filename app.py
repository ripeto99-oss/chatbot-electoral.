import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import base64
import os

# ==========================================
# 1. CONFIGURACION DE LA PAGINA
# ==========================================
st.set_page_config(page_title="Voto Informado Colombia", page_icon="🇨🇴", layout="wide")

# ==========================================
# 2. CONFIGURACION DE SEGURIDAD Y MODELO
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
        
        # Comportamiento fijo del sistema para garantizar la neutralidad electoral
        instrucciones = (
            "Eres un analista electoral neutral para Colombia. Tu objetivo es responder consultas "
            "de forma totalmente objetiva y sin sesgos politicos. Utiliza unicamente datos programaticos "
            "reales para explicar el panorama de manera educativa y equilibrada."
        )
        
        # Filtros de seguridad con las strings nativas que acepta la API sin romper la importacion
        filtros_seguridad = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucciones,
            safety_settings=filtros_seguridad
        )
    except Exception as e:
        st.error(f"Error al inicializar Gemini: {e}")
else:
    st.error("Configuracion incompleta: No se encontro la variable GEMINI_API_KEY.")

# ==========================================
# 3. CACHE DE IMAGENES
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
# 5. INTERFAZ GRAFICA (TARJETAS)
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
        "propuesta": "Enfoque de seguridad estricta, libre mercado, reduccion drastica del gasto publico, privatizaciones y defensa de las instituciones tradicionales."
    },
    {
        "col": col2, "nombre": "Ivan Cepeda", "partido": "Pacto Historico / Izquierda", "foto": "cepeda.jpg",
        "css_custom": "object-position: center 38%; transform: scale(1.1);", 
        "propuesta": "Justicia social, reformas estructurales profundas al sistema de salud y pensiones, modelo de paz total, transicion ambiental y enfoque en derechos humanos."
    },
    {
        "col": col3, "nombre": "Paloma Valencia", "partido": "Centro Democatico / Derecha", "foto": "paloma.png",
        "css_custom": "object-position: center 15%; transform: scale(0.9);",
        "propuesta": "Reforma integral a la justicia, incentivos y creditos para el sector agricola nacional, doctrina de seguridad democratica and oposicion firme a las reformas estatales de izquierda."
    },
    {
        "col": col4, "nombre": "Sergio Fajardo", "partido": "Centro / Dignidad y Compromiso", "foto": "fajardo.jpg",
        "css_custom": "object-position: center 25%; transform: scale(1.05);",
        "propuesta": "La educacion y las regiones como motores principales del desarrollo nacional, transparencia absoluta en la contratacion publica y fomento de la innovacion tecnologica y cientifica."
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
                <div class="partido-candidato"><b>Linea/Partido:</b><br>{cand['partido']}</div>
                <p class="propuesta-candidato"><i>Enfoque:</i> {cand['propuesta']}</p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 6. SISTEMA DE CHAT SECUENCIAL
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Consulta al Asistente Electoral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostramos el historial guardado en la sesión
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura de datos limpia y sin bucles de refresco
user_prompt = st.chat_input("Preguntame sobre Abelardo, Cepeda, Paloma o Fajardo...")

if user_prompt:
    # Mostramos y guardamos el mensaje del usuario inmediatamente
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if GOOGLE_API_KEY:
        contexto_datos = (
            f"Contexto programatico colombiano:\n"
            f"- Abelardo de la Espriella: {candidatos[0]['propuesta']}\n"
            f"- Ivan Cepeda: {candidatos[1]['propuesta']}\n"
            f"- Paloma Valencia: {candidatos[2]['propuesta']}\n"
            f"- Sergio Fajardo: {candidatos[3]['propuesta']}\n\n"
            f"Pregunta del ciudadano: {user_prompt}"
        )
        
        # Generamos la respuesta directamente en su caja correspondiente
        with st.chat_message("assistant"):
            with st.spinner("Pensando respuesta neutral..."):
                try:
                    response = model.generate_content(
                        contexto_datos,
                        request_options={"timeout": 15.0}
                    )
                    
                    if response and hasattr(response, 'text') and response.text:
                        bot_response = response.text
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        st.warning("La API de Google no devolvio texto. Puede deberse a limites de cuota de la llave.")
                except Exception as e:
                    st.error(f"Fallo en la respuesta del modelo: {e}")
    else:
        st.warning("Falta la API Key para procesar tu consulta.")

# ==========================================
# 7. INTERFAZ INCRUSTADA
# ==========================================
st.write("---")
st.markdown("<h3 style='color: #003893;'>📊 Test de Afinidad y Matriz Programática</h3>", unsafe_allow_html=True)

html_seguro = """
<div style="background-color: #1e293b; padding: 40px; border-radius: 12px; text-align: center; font-family: sans-serif; color: white;">
    <h2 style="color: #FCD116; margin-bottom: 10px;">¿Quien merece tu voto en la Colombia de 2026?</h2>
    <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 600px; margin: 0 auto 25px auto;">
        Analiza los planes de gobierno reales de los candidatos presidenciales mediante datos estructurados y modelos algoritmicos objetivos. Sin sesgos mediaticos.
    </p>
    <div style="display: inline-block; background-color: #003893; color: white; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer;">
        Iniciar Test de Afinidad
    </div>
</div>
"""

components.html(html_seguro, height=300, scrolling=False)
