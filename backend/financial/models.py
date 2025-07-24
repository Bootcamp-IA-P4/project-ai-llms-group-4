from pydantic import BaseModel
from typing import Optional

class FinancialNewsRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /financial-news
    Define exactamente qué datos necesitamos del usuario para generar noticias financieras
    """
    topic: str
    company: str
    language: str

class FinancialNewsResponse(BaseModel):
    """
    Modelo de respuesta que devolvemos al usuario
    Incluye la noticia financiera generada + metadatos del mercado
    """
    news_content: str
    symbol: Optional[str] = None
    market_data: Optional[dict] = None
    timestamp: str