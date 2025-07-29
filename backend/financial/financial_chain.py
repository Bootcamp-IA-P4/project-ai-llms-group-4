import os
import re 
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

# Configurar el modelo Groq
groq_llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.7,
    max_tokens=500
)

def get_language_instruction(language: str) -> str:
    """
    Devuelve instrucciones específicas para cada idioma.
    
    Args:
        language: "Español", "Inglés", "Francés", "Italiano"
        
    Returns:
        str: Instrucción específica para el LLM
    """
    return {
        "Español": "Responde en español con corrección y claridad. Usa un estilo periodístico profesional.",
        "Inglés": "Respond in English with correct grammar and professional journalistic style.",
        "Francés": """
INSTRUCTION CRITIQUE: Tu dois répondre SEULEMENT en français, JAMAIS en espagnol ou anglais.
Réponds en français avec une grammaire correcte et un style journalistique professionnel.
IMPORTANT: Utilise seulement la langue française pour toute la réponse.
        """,
        "Italiano": """
INSTRUCCIÓN CRÍTICA: Devi rispondere SOLO in italiano, NEVER in Spanish or English.
Rispondi in italiano con una grammatica corretta e uno stile giornalistico professionale.
IMPORTANTE: Usa solo la lingua italiana per tutta la risposta.
        """
    }.get(language, "Responde en español con corrección y claridad.")

def clean_llm_response(raw_response: str) -> str:
    """
    Limpia la respuesta del LLM para devolver solo el contenido esencial de la noticia.
    
    Elimina:
    - Prefijos explicativos del LLM
    - Comentarios sobre la tarea
    - Metadata innecesaria
    """
    
    # Eliminar prefijos comunes del LLM
    prefixes_to_remove = [
        "Aquí tienes la noticia:",
        "Esta es la noticia:",
        "Noticia financiera:",
        "Aquí está la noticia financiera:",
        "La noticia es:",
        "Here's the news:",
        "Financial news:",
        "Voici la nouvelle:",
        "Ecco la notizia:"
    ]
    
    cleaned = raw_response.strip()
    
    for prefix in prefixes_to_remove:
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix):].strip()
    
    # Eliminar formato markdown
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)  # **texto** → texto
    cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)      # *texto* → texto
    cleaned = re.sub(r'`(.*?)`', r'\1', cleaned)        # `código` → código
    cleaned = re.sub(r'#{1,6}\s*', '', cleaned)         # # Título → Título
    cleaned = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned)  # [texto](url) → texto
    cleaned = re.sub(r'>\s*', '', cleaned)              # > cita → cita
    cleaned = re.sub(r'^[-*+]\s+', '', cleaned, flags=re.MULTILINE)  # - lista → lista
    cleaned = re.sub(r'^\d+\.\s+', '', cleaned, flags=re.MULTILINE)  # 1. lista → lista

    # Eliminar saltos de línea excesivos
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    
    # Mejorar separación de párrafos para mejor legibilidad
    lines = cleaned.split('\n')
    improved_lines = []
    
    for i, line in enumerate(lines):
        improved_lines.append(line)
        # Si la línea actual no está vacía y la siguiente tampoco, agregar salto extra
        if (line.strip() and 
            i < len(lines) - 1 and 
            lines[i + 1].strip() and 
            not line.endswith(':') and  # No duplicar en listas de datos
            len(line.strip()) > 30):     # Solo en párrafos largos
            improved_lines.append('')   # Línea vacía extra
    
    cleaned = '\n'.join(improved_lines)
    
    return cleaned.strip()

# Template principal para noticias financieras
FINANCIAL_NEWS_TEMPLATE = """
{language_instruction}

DATOS FINANCIEROS ACTUALIZADOS:
{market_data}

TAREA:
Genera una noticia financiera profesional sobre: "{topic}"

CARACTERÍSTICAS DE LA NOTICIA:
- Estilo periodístico profesional y objetivo
- Incluye datos específicos del mercado si están disponibles
- Contexto relevante y análisis básico
- Longitud: 150-300 palabras
- Información factual y precisa
- Estructura clara con párrafos bien definidos
- Disclaimer al final: "Esta información es solo educativa, no constituye consejo de inversión"

INSTRUCCIONES IMPORTANTES:
- NO uses hashtags ni emojis
- NO menciones plataformas sociales
- Enfócate en el contenido informativo
- Usa un tono neutral y profesional
- Incluye datos numéricos cuando estén disponibles

GENERA LA NOTICIA:
"""

# Crear el prompt template
news_prompt = PromptTemplate(
    input_variables=["language_instruction", "market_data", "topic"],
    template=FINANCIAL_NEWS_TEMPLATE
)

# Crear el chain de LangChain
financial_news_chain = news_prompt | groq_llm

def generate_financial_news(topic: str, language: str, market_data: str) -> str:
    """
    Función principal que orquesta la generación de noticias financieras.
    
    Esta función combina:
    - Instrucciones de idioma
    - Datos del mercado actualizados
    - El topic del usuario
    
    Y lo envía todo estructurado a Groq para generar una noticia profesional.
    """
    try:
        # Obtener instrucciones específicas de idioma
        language_instruction = get_language_instruction(language)
        
        # Ejecutar el chain de LangChain
        result = financial_news_chain.invoke({
            "language_instruction": language_instruction,
            "market_data": market_data,
            "topic": topic
        }, config={
            "tags": ["financial-news", "groq-llm"],
            "metadata": {
                "service": "financial-news",
                "language": language,
                "topic": topic
            }
        })
        
        # Extraer el contenido del resultado
        if hasattr(result, 'content'):
            raw_content = result.content
        else:
            raw_content = str(result)
        
        # Limpiar la respuesta del LLM
        clean_content = clean_llm_response(raw_content)
        return clean_content
        
    except Exception as e:
        # Fallback: noticia básica si falla Groq
        fallback_templates = {
            "Español": f"""
Noticia Financiera: {topic}

Los datos del mercado no están disponibles en este momento para proporcionar información específica sobre esta consulta financiera.

Se recomienda a los inversores mantenerse informados a través de fuentes oficiales y consultar con asesores financieros profesionales antes de tomar decisiones de inversión.

Esta información es solo educativa, no constituye consejo de inversión.
            """,
            
            "Inglés": f"""
Financial News: {topic}

Market data is currently unavailable to provide specific information about this financial query.

Investors are advised to stay informed through official sources and consult with professional financial advisors before making investment decisions.

This information is for educational purposes only, not investment advice.
            """,
            
            "Francés": f"""
Actualité Financière: {topic}

Les données de marché ne sont actuellement pas disponibles pour fournir des informations spécifiques sur cette requête financière.

Il est conseillé aux investisseurs de rester informés par des sources officielles et de consulter des conseillers financiers professionnels avant de prendre des décisions d'investissement.

Cette information est à des fins éducatives uniquement, pas des conseils en investissement.
            """,
            
            "Italiano": f"""
Notizia Finanziaria: {topic}

I dati di mercato non sono attualmente disponibili per fornire informazioni specifiche su questa richiesta finanziaria.

Si consiglia agli investitori di rimanere informati attraverso fonti ufficiali e di consultare consulenti finanziari professionali prima di prendere decisioni di investimento.

Queste informazioni sono solo educative, non costituiscono consigli di investimento.
            """
        }
        
        fallback_content = fallback_templates.get(language, fallback_templates["Español"])
        return fallback_content.strip()