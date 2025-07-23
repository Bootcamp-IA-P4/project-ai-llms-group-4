from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from .generate_with_rag import generate_text_with_context
from .image_generator import generate_image_url


app = FastAPI()

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
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
    return {"message": "✅ API en funcionamiento"}

@app.post("/generate")
def generate_content(data: ContentRequest):
    # Generar el contenido textual
    result_text = generate_text_with_context(
        topic=data.topic,
        platform=data.platform,
        company=data.company,
        tone=data.tone,
        language=data.language,
        model=data.model,
        audience=data.audience
    )

    # Generar la imagen solo si se marca como True
    image_url = None
    if data.generate_image:
        image_url = generate_image_url(
            topic=data.topic,
            platform=data.platform,
            tone=data.tone,
            audience=data.audience
        )

    return {
        "text": result_text,
        "image": image_url
    }
