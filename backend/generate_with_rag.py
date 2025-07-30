import os
from dotenv import load_dotenv
from backend.vector_db.db_manager import search_similar 
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

def generate_text_with_context(topic, platform, tone, company, language, model, img_model, audience=None, extra_context=None):

    """
    Genera contenido adaptado al contexto del usuario.
    Utiliza información anterior desde Pinecone si existe, y adapta el estilo al tono, empresa, plataforma y audiencia indicadas.
    """
    company_clean = company.strip().lower() if company else ""
    language_instruction = get_language_instruction(language)

    # 🧩 Añadir audiencia si está presente
    audience_text = f"\nLa audiencia objetivo es: {audience}, utiliza lenguaje específico para esta audiencia." if audience else ""

    # Construcción del mensaje principal
    message_base = f"""Escribe un contenido para la plataforma {platform}, sobre el tema: "{topic}"."""

    # Recuperar contexto relevante desde Pinecone (por score y empresa)
    context_text = ""
    try:
        context_results = search_similar(topic, top_k=5)
        score_minimo = 0.65
        empresa_actual = company_clean if company_clean else None

        contexto_filtrado = [
            doc.page_content for doc, score in context_results
            if score >= score_minimo
            and (not empresa_actual or doc.metadata.get("company", "").lower() == empresa_actual)
        ]

        if contexto_filtrado:
            context_text = "\n".join(contexto_filtrado)
            print("🧠 Contexto añadido al prompt desde Pinecone:\n")
            for fragmento in contexto_filtrado:
                print(f"- {fragmento[:120]}...")

    except Exception as e:
        print(f"⚠️ Error al recuperar contexto desde Pinecone: {e}")

         # Añadir contexto adicional del documento (extra_context)
    extra_context_text = f"\nContexto adicional proporcionado por el usuario:\n{extra_context.strip()}" if extra_context else ""

    # Construcción del prompt con contexto semántico relevante (si existe)
    contexto_extra = f"\nContexto relevante de publicaciones anteriores:\n{context_text}\n" if context_text else ""

    full_prompt = f"""{language_instruction}
{contexto_extra}{extra_context_text}
{message_base}{audience_text}
Usa un tono {tone.lower()} y adapta el mensaje como si fuera publicado por {company if company else "una empresa"}.
Debe ser directo, atractivo y adecuado para esa red social."""

    return generate_text(full_prompt, model), full_prompt
