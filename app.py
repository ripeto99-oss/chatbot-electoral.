from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os
import uvicorn

app = FastAPI()

# Servir archivos estáticos (CSS y JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ==========================================
# MODELOS DE PYDANTIC PARA VALIDACIÓN
# ==========================================
class ChatContext(BaseModel):
    resultado: str
    candidato_top: str
    afinidad: int
    ranking: list
    respuestas_usuario: dict

class ChatRequest(BaseModel):
    message: str
    context: ChatContext

# Configuración Inicial de Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Parámetros nombrados para compatibilidad total con Starlette/Render
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not GEMINI_API_KEY:
        return {"response": "Error: La API Key de Gemini no está configurada en las variables de entorno de Render."}
    
    try:
        # Identificador técnico exacto para los modelos actuales de tu cuenta
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Construimos el Prompt del Sistema inyectando los resultados del usuario
        ranking_str = ", ".join([f"{r['name']} ({r['overallMatch']}%)" for r in req.context.ranking])
        
        system_prompt = f"""
        Eres un analista político neutral y experto de 'Voto Informado 2.0'.
        Tu objetivo es ayudar al usuario a entender sus resultados electorales de las elecciones de Colombia 2026.
        
        CONTEXTO DEL USUARIO:
        - Su candidato de mayor afinidad es: {req.context.candidato_top} ({req.context.afinidad}% de afinidad).
        - Su ranking completo es: {ranking_str}.
        
        REGLAS:
        1. Responde de manera clara, objetiva y sin sesgos políticos.
        2. Basa tus respuestas en el contexto dado. Si el usuario pregunta por qué le salió un candidato, asocia sus respuestas con el perfil del candidato.
        3. Sé conciso y conversacional. No des discursos largos.
        4. NUNCA inventes posturas políticas que no estén en el contexto.
        """
        
        # Combinamos el rol del sistema y el mensaje del usuario
        full_prompt = f"{system_prompt}\n\nPregunta del Usuario: {req.message}"
        
        response = model.generate_content(full_prompt)
        return {"response": response.text}
        
    except Exception as e:
        print(f"Error en Gemini API: {e}")
        return {"response": "Lo siento, tuve un problema interno al analizar tus datos. Por favor, intenta de nuevo."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
