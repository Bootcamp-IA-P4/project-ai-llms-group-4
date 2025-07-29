from backend.vector_db.db_manager import search_similar
from backend.generator import generate_text
from backend.image_generator import generate_image_url

def get_language_instruction(language):
    return {
        "Español": "Comunícate en español de manera natural y fluida, como si estuvieras conversando con alguien que valoras mucho.",
        "Inglés": "Communicate in English with warmth and authenticity, as if you're having a friendly conversation with someone you care about.",
        "Francés": "Communique en français avec chaleur et authenticité, comme si tu avais une conversation amicale avec quelqu'un qui te tient à cœur.",
        "Italiano": "Comunica in italiano con calore e autenticità, come se stessi avendo una conversazione amichevole con qualcuno a cui tieni."
    }.get(language, "Comunícate en español de manera natural y fluida, como si estuvieras conversando con alguien que valoras mucho.")

# def get_tone_guidance(tone):
#     tone_guides = {
#         "profesional": "Adopta un tono profesional pero cálido. Sé experto sin ser intimidante, confiable sin ser rígido.",
#         "casual": "Usa un tono relajado y conversacional, como si estuvieras charlando con un buen amigo sobre algo que te apasiona.",
#         "formal": "Mantén un registro formal pero no frío. Sé respetuoso, preciso y elegante en tu expresión.",
#         "divertido": "Sé entretenido y ligero, pero siempre manteniendo el valor del contenido. Usa humor inteligente cuando sea apropiado.",
#         "educativo": "Adopta el tono de un mentor paciente que genuinamente quiere que su audiencia aprenda y crezca.",
#         "inspiracional": "Sé motivador y positivo, pero auténtico. Evita clichés y enfócate en insights reales y valiosos."
#     }
#     return tone_guides.get(tone.lower(), "Mantén un tono equilibrado que sea apropiado para el contexto y la audiencia.")

def research_agent(topic: str, company: str, top_k: int = 3, model: str = "llama3-8b-8192") -> str:
    if company and company.strip().lower() == "ruiztech":
        context_results = search_similar(topic, top_k=top_k)

        context = "\n".join([doc.page_content for doc, _ in context_results])

        return context
    return ""


def writing_agent(topic, platform, tone, company, language, audience, context, model: str) -> (str, str):
    instruction = get_language_instruction(language)
    audience_text = f"\n🎯 Tu audiencia son: {audience}. Habla su idioma, entiende sus necesidades y conecta con sus intereses genuinos." if audience else ""
    company_text = f"representando la voz auténtica de {company}" if company else "manteniendo una voz profesional pero accesible"
    context_text = f"\n📚 **Información de contexto relevante:**\n{context}\n" if context else ""

    base_prompt = f"""{instruction}

{context_text}

Escribe un contenido para la plataforma {platform}, sobre el tema: "{topic}".
Usa un tono {tone.lower()} y adáptalo {company_text}.{audience_text}
Debe ser directo, atractivo y adecuado para esa audiencia {audience}."""

    model = "llama-3.3-70b-versatile"
    text = generate_text(base_prompt, model=model)
    return text, base_prompt


def image_agent(prompt: str, model: str = "stability") -> str:
    return generate_image_url(prompt, model)
