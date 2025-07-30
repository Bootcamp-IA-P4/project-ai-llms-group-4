import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from langsmith import traceable

# Cargar variables de entorno desde .env en la raíz del proyecto
load_dotenv()

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
    "Content-Type": "application/json"
}

@traceable(name="Llamada al LLM vía Groq")
def generate_text(prompt, model):
    payload = {
        "model": model,
        "messages": [
            {"role": "system",
              "content": f"""Eres un creador de contenido experto y empático, especializado en adaptar mensajes para diferentes plataformas digitales y audiencias diversas.

            🌟 **Tu misión es:**
            - Crear contenido auténtico que resuene emocionalmente con la audiencia
            - Adaptar perfectamente el mensaje al formato y cultura de cada plataforma
            - Mantener siempre un equilibrio entre profesionalismo y calidez humana
            - Ofrecer valor real en cada palabra que escribes

            🎨 **Tu estilo de trabajo:**
            - Eres creativo pero estratégico
            - Entiendes las sutilezas de la comunicación digital
            - Sabes cuándo ser directo y cuándo ser más elaborado
            - Siempre priorizas la claridad sin sacrificar el engagement

            """},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Parse Error: {str(e)} | Raw Response: {response.text}"
    else:
        return f"❌ API Error: {response.status_code} | {response.text}"

