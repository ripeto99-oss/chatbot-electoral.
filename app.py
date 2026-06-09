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
        
        # Construimos un string con el ranking para contexto
        ranking_str = ", ".join([f"{r['name']} ({r.get('overallMatch', 0)}%)" for r in req.context.ranking])
        
        # Extraer puntajes específicos de los finalistas para la Segunda Vuelta
        afinidad_cepeda = next((r.get('overallMatch', 0) for r in req.context.ranking if r['name'] == 'Iván Cepeda'), 0)
        afinidad_espriella = next((r.get('overallMatch', 0) for r in req.context.ranking if r['name'] == 'Abelardo de la Espriella'), 0)
        
        # NUEVO PROMPT MAESTRO - MODO SEGUNDA VUELTA
        system_prompt = f"""
        Eres un Asistente Electoral experto y neutral para las Elecciones Presidenciales de Colombia 2026.
        ESTAMOS EN UN ESCENARIO DE SEGUNDA VUELTA (BALOTAJE). 
        
        CONTEXTO DEL USUARIO:
        - Respuestas de su test: {req.context.respuestas_usuario}
        - Afinidad en 2da vuelta -> Cepeda: {afinidad_cepeda}% | De la Espriella: {afinidad_espriella}%
        - Ranking general original: {ranking_str}
        
        REGLAS ESTRICTAS:
        1. SOLO hay dos candidatos vivos en esta elección: Iván Cepeda (Pacto Histórico - Izquierda Estructural) y Abelardo de la Espriella (Defensores de la Patria - Derecha Soberanista).
        2. Sergio Fajardo y Paloma Valencia FUERON ELIMINADOS en la primera vuelta. NUNCA recomiendes votar por ellos. Si el usuario pregunta por ellos, explícale que debe decidir entre los dos finalistas.
        3. Tu objetivo es ayudar al usuario a entender el contraste extremo entre estos dos candidatos en temas clave basados en sus respuestas.
        4. Responde de manera clara, objetiva, concisa y conversacional. No des discursos largos ni emitas juicios de valor sobre ninguna ideología.
        5. NUNCA inventes posturas políticas que no estén verificadas.
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
