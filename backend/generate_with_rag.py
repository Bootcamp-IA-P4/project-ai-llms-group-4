import os
from dotenv import load_dotenv
from backend.agents.agent import writing_agent, research_agent
from langsmith import traceable

load_dotenv()

@traceable(name="Generación de texto con contexto RAG")
def generate_text_with_context(
    topic,
    platform,
    tone,
    company,
    language,
    model_writer,
    model_research,
    audience=None
):
    context = research_agent(topic, company, model=model_research)
    text, prompt = writing_agent(topic, platform, tone, company, language, audience, context, model=model_writer)
    return text, prompt
