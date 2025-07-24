import os
from dotenv import load_dotenv
from backend.retriever import get_relevant_chunks
from backend.generator import generate_text

# Cargar variables de entorno si se requieren
load_dotenv()

def get_language_instruction(language):
    """
    Devuelve la instrucción de idioma apropiada para el LLM.
    """
    return {
        "Español": "Responde en español con corrección y claridad.",
        "Inglés": "Respond in English with correct grammar and natural style.",
        "Francés": "Réponds en français avec une grammaire correcte et un style naturel.",
        "Italiano": "Rispondi in italiano con una grammatica corretta e uno stile naturale."
    }.get(language, "Responde en español con corrección y claridad.")

def generate_text_with_context(topic, platform, tone, company, language, model,img_model, audience=None):
    """
    Genera contenido adaptado al contexto si la empresa es RuizTech.
    También incorpora información sobre la audiencia objetivo.
    """
    company_clean = company.strip().lower()
    is_ruiztech = company_clean == "ruiztech"
    language_instruction = get_language_instruction(language)

    # 🧩 Añadir audiencia si está presente
    audience_text = f"\nLa audiencia objetivo es: {audience}, utiliza lenguaje específico para esta audiencia" if audience else ""

    # Construcción del mensaje principal
    message_base = f"""Escribe un contenido para la plataforma {platform}, sobre el tema: "{topic}"."""

    if is_ruiztech:
        context = get_relevant_chunks(topic)
        full_prompt = f"""{language_instruction}

Contexto relevante de la empresa RuizTech:
{context}

{message_base}{audience_text}
Usa un tono {tone.lower()}, y adapta el mensaje como si fuera publicado por RuizTech.
Debe ser directo, atractivo y adecuado para esa red social."""
    else:
        full_prompt = f"""{language_instruction}
{message_base}{audience_text}
Usa un tono {tone.lower()} y adapta el mensaje como si fuera publicado por {company if company else "una empresa"}.
Debe ser directo, atractivo y adecuado para esa red social."""

    # Retorna también el prompt para mostrarlo en la app
    return generate_text(full_prompt, model), full_prompt

