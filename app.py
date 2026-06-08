from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os
import uvicorn

# 1. CONFIGURACIÓN DE LA APLICACIÓN
app = FastAPI(title="Voto Informado Backend")

# Montar carpetas de estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 2. MODELOS DE DATOS (Pydantic)
class ChatContext(BaseModel):
    resultado: str = "Desconocido"
    candidato: str = "Desconocido"
    afinidad: int = 0

class ChatRequest(BaseModel):
    message: str
    context: ChatContext

# 3. CONFIGURACIÓN DE SEGURIDAD (API KEY)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error al inicializar Gemini: {e}")
        model = None
else:
    print("Advertencia: No se encontró la variable de entorno GEMINI_API_KEY.")
    model = None

# 4. RUTAS Y ENDPOINTS
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Sirve el index.html principal como SPA"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Endpoint REST real para procesar peticiones hacia Gemini"""
    if not model:
        return {"response": "Error interno: El servidor no tiene configurada la clave API de Gemini."}
    
    try:
        # Construcción del prompt inyectando el contexto del usuario (sin sesgos)
        system_prompt = f"""
        Eres un analista electoral colombiano experto, neutral y objetivo.
        El usuario está consultando sobre las elecciones presidenciales de 2026.
        Contexto del test ciudadano actual: 
        Su mayor afinidad algorítmica es con el candidato {request.context.candidato} ({request.context.afinidad}% de coincidencia).
        
        Instrucciones:
        - Responde la pregunta del usuario de forma directa y accesible.
        - Basate en los planes de gobierno reales de los candidatos.
        - Mantén neutralidad absoluta, no sugieras por quién votar.
        """
        
        # Iniciar chat con contexto
        chat = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Entendido. Operaré como analista neutral basándome en los datos programáticos."]}
        ])
        
        # Enviar el mensaje real del usuario
        response = chat.send_message(request.message)
        
        return {"response": response.text}
        
    except Exception as e:
        return {"response": f"Fallo en la comunicación con la IA: {str(e)}"}

# 5. EJECUCIÓN DEL SERVIDOR
if __name__ == "__main__":
    # Iniciar servidor en el puerto 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
