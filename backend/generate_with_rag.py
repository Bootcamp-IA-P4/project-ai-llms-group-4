import os
from dotenv import load_dotenv
from backend.retriever import get_relevant_chunks
from backend.generator import generate_text

# Load environment variables if needed
load_dotenv()

def get_language_instruction(language):
    """
    Returns the appropriate language instruction for the LLM, encouraging a simple, casual, yet respectful style.
    """
    instructions = {
        "Español": "Responde en español de forma sencilla, cercana y respetuosa, asegurándote de transmitir un mensaje positivo y claro.",
        "Inglés": "Respond in English in a simple, casual, and respectful way, always sharing a good and clear message.",
        "Francés": "Réponds en français de façon simple, naturelle et respectueuse, tout en transmettant un message positif et clair.",
        "Italiano": "Rispondi in italiano in modo semplice, naturale e rispettoso, assicurandoti di trasmettere un messaggio positivo e chiaro."
    }
    return instructions.get(language, instructions["Español"])

def generate_text_with_context(topic, platform, tone, company, language, model, audience=None):
    """
    Generates content tailored to the context, company, platform, and target audience.
    Focuses on delivering messages in a casual, simple, and welcoming way with natural connectors.
    """
    company_clean = company.strip().lower()
    is_ruiztech = company_clean == "ruiztech"
    language_instruction = get_language_instruction(language)

    # 🧩 Audience addition
    audience_text = f"\nLa audiencia objetivo es: {audience}. Utiliza un lenguaje sencillo, cercano y enfocado en esta audiencia para que se sientan cómodos y bienvenidos." if audience else ""

    # 🔗 Message construction with natural connectors
    message_base = (
        f"Escribe un contenido para la plataforma {platform}, sobre el tema: \"{topic}\". "
        "Conecta las ideas de manera natural, usando frases y transiciones que hagan sentir al lector cómodo y acompañado. "
        "Siempre mantén un tono casual y respetuoso, como si hablaras con un amigo, pero transmitiendo profesionalismo."
    )

    # 🏢 RuizTech context inclusion
    if is_ruiztech:
        context = get_relevant_chunks(topic)
        full_prompt = (
            f"{language_instruction}\n\n"
            "Aquí tienes el contexto relevante de la empresa RuizTech para inspirarte y aportar valor:\n"
            f"{context}\n\n"
            f"{message_base}{audience_text}\n"
            f"Usa un tono {tone.lower()}, asegurándote de que el mensaje suene como RuizTech: directo, atractivo, cálido y adecuado para {platform}."
        )
    else:
        full_prompt = (
            f"{language_instruction}\n\n"
            f"{message_base}{audience_text}\n"
            f"Usa un tono {tone.lower()} y adapta el mensaje como si fuera publicado por {company if company else 'una empresa'}."
            f" Hazlo directo, atractivo y adecuado para {platform}."
        )

    # Return generated text and the final prompt for display
    return generate_text(full_prompt, model), full_prompt