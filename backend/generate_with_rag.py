import os
from dotenv import load_dotenv
from backend.agents.agent import writing_agent, research_agent

load_dotenv()

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
