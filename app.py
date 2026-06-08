from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os
import uvicorn

app = FastAPI(title="Voto Informado 2.0")

# Servir archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración IA
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

class ChatRequest(BaseModel):
    message: str
    context: dict

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/api/chat")
async def chat_api(request: ChatRequest):
    if not model:
        return {"error": "API Key de Gemini no está configurada en Render."}

    try:
        ctx = request.context
        candidato = ctx.get("resultado_principal", "Ninguno")
        ranking = ctx.get("ranking", [])
        
        system_prompt = f"""
        Eres el 'Asistente Electoral IA', un experto en política colombiana, neutral y analítico.
        Los candidatos de este test son: Abelardo, Cepeda, Paloma, y Fajardo.
        
        Contexto del usuario actual:
        Candidato más afín: {candidato}
        Ranking completo: {', '.join(ranking)}
        
        Responde a la pregunta del usuario basándote en este contexto. Si pregunta por qué es afín a un candidato, explícalo de forma general y respetuosa.
        
        Pregunta del usuario: {request.message}
        """
        
        response = model.generate_content(system_prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": f"Fallo interno de IA: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
