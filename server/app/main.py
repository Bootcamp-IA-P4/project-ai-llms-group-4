from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Modelo de entradaS
class ContentRequest(BaseModel):
    topic: str
    platform: str
    company: Optional[str] = None
    tone: str
    language: str
    audience: Optional[str] = None
    model: str
    generate_image: bool = True

@app.get("/")
def read_root():
    return {"message": "API en funcionamiento"}

@app.post("/generate")
def generate_content(data: ContentRequest):
    # Conectar con generate_text_with_context o la función que se establezca si hay cambios
    return {
        "prompt_base": f"Contenido solicitado para el tema '{data.topic}' en la plataforma {data.platform}."
    }
