from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from .generate_with_rag import generate_text_with_context
from .image_generator import generate_image_url
from backend.financial.models import FinancialNewsRequest
from backend.financial.financial_service import generate_financial_news


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
    # Obtener solo el texto generado (ignoramos el prompt)
    text, _ = generate_text_with_context(
        topic=data.topic,
        platform=data.platform,
        company=data.company,
        tone=data.tone,
        language=data.language,
        model=data.model,
        audience=data.audience
    )

    image_url = None
    if data.generate_image:
        # Solo pasamos el texto generado
        image_url = generate_image_url(text)

    return {
        "text": text,
        "image": image_url
    }

# Endpoint para noticias financieras
@app.post("/financial-news")
def financial_news_endpoint(data: FinancialNewsRequest):
    """
    - Recibe: topic, company, language
    - Devuelve: noticia financiera profesional con datos actualizados para la empresa específica
    """
    return generate_financial_news(data)