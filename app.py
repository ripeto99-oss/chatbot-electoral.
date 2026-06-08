from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os
import uvicorn

app = FastAPI(title="Voto Informado Backend")

# Montar estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configurar Gemini
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Usamos un modelo rápido y estable
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# Modelo de datos para recibir el mensaje del frontend
class ChatRequest(BaseModel):
    message: str
    context: dict

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Corrección del error de Render: se pasan los argumentos correctamente
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@app.post("/api/chat")
async def chat_endpoint(chat_req: ChatRequest):
    if not model:
        return {"error": "API Key de Gemini no configurada en el servidor de Render."}

    try:
        # Extraemos el contexto de los resultados del usuario
        ctx = chat_req.context
        candidato = ctx.get("resultado_principal", "Desconocido")
        afinidad = ctx.get("porcentaje_afinidad", "0")
        
        # Prompt de sistema invisible para darle contexto a Gemini
        system_prompt = f"""
        Eres un Asistente Electoral IA neutral y objetivo para Colombia.
        Los candidatos evaluados en este test son: Abelardo, Cepeda, Paloma, y Fajardo.
        El usuario acaba de terminar su test. Su candidato más afín es {candidato} con un {afinidad}% de afinidad.
        Ayuda al usuario a entender sus resultados o responde sus dudas sobre los candidatos de forma respetuosa y sin sesgos.
        
        Pregunta del usuario: {chat_req.message}
        """
        
        response = model.generate_content(system_prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": f"Error procesando la solicitud: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
