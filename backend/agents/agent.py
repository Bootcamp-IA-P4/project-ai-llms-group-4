from vector_db.db_manager import search_similar
from generator import generate_text
from image_generator import generate_image_url

def get_language_instruction(language):
    return {
        "Español": "Comunícate en español de manera natural y fluida, como si estuvieras conversando con alguien que valoras mucho.",
        "Inglés": "Communicate in English with warmth and authenticity, as if you're having a friendly conversation with someone you care about.",
        "Francés": "Communique en français avec chaleur et authenticité, comme si tu avais une conversation amicale avec quelqu'un qui te tient à cœur.",
        "Italiano": "Comunica in italiano con calore e autenticità, come se stessi avendo una conversazione amichevole con qualcuno a cui tieni."
    }.get(language, "Comunícate en español de manera natural y fluida, como si estuvieras conversando con alguien que valoras mucho.")

def research_agent(topic: str, company: str, top_k: int = 5, model: str = "llama3-8b-8192") -> str:
        context_text = ""
        try:
            company_clean = company.strip().lower() if company else ""
            context_results = search_similar(topic, top_k=top_k)
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
    
        return context_text


def writing_agent(topic, platform, tone, company, language, audience, context, model: str, extra_context: str = "") -> tuple[str, str]:
    instruction = get_language_instruction(language)
    audience_text = f"\n🎯 Tu audiencia son: {audience}. Habla su idioma, entiende sus necesidades y conecta con sus intereses genuinos." if audience else ""
    company_text = f"representando la voz auténtica de {company}" if company else "manteniendo una voz profesional pero accesible"
    context_text = f"\n📚 **Información de contexto relevante:**\n{context}\n" if context else ""
    extra_context_text = f"\n📎 Contexto adicional proporcionado por el usuario:\n{extra_context.strip()}" if extra_context else ""

    base_prompt = f"""{instruction}

{context_text}{extra_context_text}

Escribe un contenido para la plataforma {platform}, sobre el tema: "{topic}" solo adaptate a ese tema, da la informacion que consideres necesaria y basate solo en lo que pide el usuario.
Usa un tono {tone.lower()} y adáptalo {company_text}.{audience_text}
Debe ser directo, atractivo y adecuado para esa audiencia {audience}."""

    model = "llama-3.3-70b-versatile"
    text = generate_text(base_prompt, model=model)
    return text, base_prompt
