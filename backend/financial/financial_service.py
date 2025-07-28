import os
from datetime import datetime
from typing import Dict, Any
from .models import FinancialNewsRequest
from .financial_tools import get_stock_data, format_market_data_for_llm
from .financial_chain import generate_financial_news as generate_news_with_llm
import time

def generate_financial_news(request: FinancialNewsRequest) -> Dict[str, Any]:
    """
    Función principal del servicio de noticias financieras.
    
    Esta es la función orquestadora que:
    1. Recibe la petición del usuario (topic, company, language)
    2. Obtiene datos financieros en tiempo real para la empresa específica
    3. Formatea los datos para el LLM
    4. Genera la noticia financiera profesional
    5. Devuelve todo estructurado
    
    Es el "director de orquesta" que coordina todos los demás archivos.
    """
    
    try:
        # 1. Obtener datos financieros para la empresa específica
        stock_data = get_stock_data(request.company)
        symbol = stock_data.get("symbol", "UNKNOWN")
        company_name = stock_data.get("company_name", request.company)
        
        # 2. Formatear datos para el LLM
        formatted_market_data = format_market_data_for_llm(stock_data)
        
        # 3. Generar noticia financiera
        generated_news = generate_news_with_llm(
            topic=request.topic,
            language=request.language,
            market_data=formatted_market_data
        )
        
        # 4. Estructurar respuesta final
        response_data = {
            "news_content": generated_news,
            "symbol": symbol,
            "market_data": {
                "symbol": symbol,
                "company_name": company_name,
                "success": stock_data.get("success", False),
                "timestamp": stock_data.get("timestamp", datetime.now().isoformat()),
                "has_real_data": stock_data.get("success", False),
                "source": stock_data.get("source", "unknown")
            },
            "timestamp": datetime.now().isoformat(),
            "request_info": {
                "original_topic": request.topic,
                "company": request.company,
                "language": request.language
            }
        }

        # 5. Guardar en base de datos
        start_time = time.time()
        processing_time_ms = int((time.time() - start_time) * 1000)

        from backend.database.repository import save_financial_news_record
        try:
            save_financial_news_record(
                request=request,
                response_data=response_data, 
                processing_time_ms=processing_time_ms,
                success=True
            )
        except Exception as e:
            # Error guardando en BD (no crítico)
            pass
        
        return response_data
        
    except Exception as e:
        # Sistema de fallback
        return create_fallback_news_response(request, str(e))

def create_fallback_news_response(request: FinancialNewsRequest, error_message: str) -> Dict[str, Any]:
    """
    Crea una respuesta de fallback cuando algo falla.
    
    Principio: El sistema NUNCA debe devolver error 500 al usuario.
    Siempre devuelve una noticia útil, aunque sea básica.
    """
    
    # Noticias de fallback según idioma
    fallback_news_templates = {
        "Español": """
Noticia Financiera: {topic} - {company}

Los mercados financieros continúan presentando movimientos significativos en el sector relacionado con {company}.

Debido a la volatilidad actual del mercado, no se dispone de datos específicos en tiempo real para {company} en este momento.

Los analistas recomiendan a los inversores mantenerse informados a través de fuentes oficiales y realizar un seguimiento cuidadoso de los indicadores económicos relevantes antes de tomar decisiones de inversión.

El contexto macroeconómico actual sugiere la importancia de diversificar las carteras y considerar tanto los riesgos como las oportunidades en el mercado actual.

Esta información es solo educativa, no constituye consejo de inversión.
        """,
        
        "Inglés": """
Financial News: {topic} - {company}

Financial markets continue to show significant movements in the sector related to {company}.

Due to current market volatility, specific real-time data for {company} is not available at this time.

Analysts recommend that investors stay informed through official sources and carefully monitor relevant economic indicators before making investment decisions.

The current macroeconomic context suggests the importance of diversifying portfolios and considering both risks and opportunities in the current market.

This information is for educational purposes only, not investment advice.
        """,
        
        "Francés": """
Actualité Financière: {topic} - {company}

Les marchés financiers continuent de présenter des mouvements significatifs dans le secteur lié à {company}.

En raison de la volatilité actuelle du marché, les données spécifiques en temps réel pour {company} ne sont pas disponibles en ce moment.

Les analystes recommandent aux investisseurs de rester informés par des sources officielles et de surveiller attentivement les indicateurs économiques pertinents avant de prendre des décisions d'investissement.

Le contexte macroéconomique actuel suggère l'importance de diversifier les portefeuilles et de considérer à la fois les risques et les opportunités du marché actuel.

Cette information est à des fins éducatives uniquement, pas des conseils en investissement.
        """,
        
        "Italiano": """
Notizia Finanziaria: {topic} - {company}

I mercati finanziari continuano a mostrare movimenti significativi nel settore relativo a {company}.

A causa dell'attuale volatilità del mercado, i dati specifici in tempo reale per {company} non sono disponibili in questo momento.

Gli analisti raccomandano agli investitori di rimanere informati attraverso fonti ufficiali e di monitorare attentamente gli indicatori economici rilevanti prima di prendere decisioni di investimento.

Il contesto macroeconomico attuale suggerisce l'importanza di diversificare i portafogli e considerare sia i rischi che le opportunità nel mercato attuale.

Queste informazioni sono solo educative, non costituiscono consigli di investimento.
        """
    }
    
    # Seleccionar template según idioma
    template = fallback_news_templates.get(
        request.language, 
        fallback_news_templates["Español"]
    )
    
    fallback_news = template.format(
        topic=request.topic,
        company=request.company
    ).strip()
    
    response_data = {
        "news_content": fallback_news,
        "symbol": "UNKNOWN",
        "market_data": {
            "symbol": "UNKNOWN",
            "company_name": request.company,
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "has_real_data": False,
            "source": "fallback"
        },
        "timestamp": datetime.now().isoformat(),
        "request_info": {
            "original_topic": request.topic,
            "company": request.company,
            "language": request.language
        },
        "is_fallback": True
    }
    
    return response_data