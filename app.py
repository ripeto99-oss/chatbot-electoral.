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
# 2. CONFIGURACION DE SEGURIDAD Y LLAVE
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]
else:
    GOOGLE_API_KEY = None

SYSTEM_INSTRUCTION = (
    "Eres un analista electoral neutral para Colombia. Tu objetivo es responder consultas "
    "de forma totalmente objetiva y sin sesgos politicos. Utiliza unicamente datos programaticos "
    "reales para explicar el panorama de manera educativa y equilibrada."
)

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
# 6. CHAT POR REQUESTS DIRECTO (SOPORTA AQ O CUALQUIERA)
# ==========================================
st.markdown("<h3 style='color: #003893;'>💬 Consulta al Asistente Electoral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Preguntame sobre Abelardo, Cepeda, Paloma o Fajardo...")

if user_prompt:
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
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando respuesta neutral..."):
                try:
                    # Endpoint REST directo. Al meter la llave en la URL, Google la procesa sin importar el formato
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                    headers = {"Content-Type": "application/json"}
                    
                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {"text": contexto_datos}
                                ]
                            }
                        ],
                        "systemInstruction": {
                            "parts": [
                                {"text": SYSTEM_INSTRUCTION}
                            ]
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=payload)
                    res_data = response.json()
                    
                    if response.status_code == 200:
                        bot_response = res_data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        st.error(f"Error de autenticación o respuesta de Google (Código {response.status_code}):")
                        st.json(res_data)
                        
                except Exception as e:
                    st.error(f"Error en la conexión HTTP:")
                    st.code(str(e))
    else:
        st.warning("No se encontró la llave GEMINI_API_KEY en los Secrets.")

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
