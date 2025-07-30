from typing import List, Optional, Dict, Any
from supabase_client import get_supabase_client
from financial.models import FinancialNewsRequest

def save_financial_news_record(
    request: FinancialNewsRequest,
    response_data: Dict[str, Any],
    processing_time_ms: int,
    success: bool = True,
    error_message: Optional[str] = None
) -> bool:
    """
    Guarda un registro de noticia financiera en Supabase.
    
    Args:
        request: La petición original del usuario
        response_data: Los datos de respuesta generados
        processing_time_ms: Tiempo de procesamiento en milisegundos
        success: Si la operación fue exitosa
        error_message: Mensaje de error si hubo alguno
        
    Returns:
        bool: True si se guardó exitosamente, False si no
    """
    
    try:
        client = get_supabase_client()
        if not client:
            print("⚠️ Cliente Supabase no disponible")
            return False
        
        # Extraer datos del response
        market_data = response_data.get("market_data", {})
        
        # Preparar registro
        record = {
            # Input del usuario
            "topic": request.topic,
            "company": request.company,
            "language": request.language,
            
            # Resultado financiero
            "symbol": response_data.get("symbol"),
            "company_resolved": market_data.get("company_name"),
            "data_source": market_data.get("source"),
            "has_real_data": market_data.get("has_real_data", False),
            
            # Contenido generado
            "news_content": response_data.get("news_content", ""),
            "content_length": len(response_data.get("news_content", "")),
            
            # Datos del mercado (JSON)
            "market_data": market_data,
            
            # Status y debugging
            "success": success,
            "error_message": error_message,
            "processing_time_ms": processing_time_ms
        }
        
        # Insertar en Supabase
        result = client.table('financial_news').insert(record).execute()
        
        print(f"✅ Registro guardado en Supabase (ID: {result.data[0]['id'] if result.data else 'N/A'})")
        return True
        
    except Exception as e:
        print(f"❌ Error guardando en Supabase: {e}")
        return False

def get_recent_financial_news(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Obtiene las noticias financieras más recientes.
    
    Args:
        limit: Número máximo de registros
        
    Returns:
        List: Lista de registros de noticias ordenados por fecha
    """
    
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        result = (client.table('financial_news_formatted')
                 .select("*")
                 .order('created_at_formatted', desc=True)
                 .limit(limit)
                 .execute())
        
        return result.data
        
    except Exception as e:
        print(f"❌ Error consultando noticias recientes: {e}")
        return []