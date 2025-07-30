from pydantic import BaseModel
from typing import Optional, Dict, Any

class FinancialNewsRecord(BaseModel):
    """
    Modelo para guardar un registro de noticia financiera en Supabase.
    Define la estructura de datos que se almacenará en la tabla 'financial_news'.
    """
    
    # Input del usuario
    topic: str
    company: str
    language: str
    
    # Resultado financiero
    symbol: Optional[str] = None
    company_resolved: Optional[str] = None  # Nombre completo de la API
    data_source: Optional[str] = None  # "polygon" | "twelve_data" | "fallback"
    has_real_data: bool = False
    
    # Contenido generado
    news_content: str
    content_length: int
    
    # Datos del mercado (JSON)
    market_data: Optional[Dict[str, Any]] = None
    
    # Status y debugging
    success: bool = True
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None
    
    # Metadata (se llenarán automáticamente en Supabase)
    # created_at y updated_at se manejan en la BD
    
    class Config:
        # Permitir campos extra por si añadimos más datos
        extra = "allow"