import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env en la raíz del proyecto
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json"
}

def generate_text(prompt, model):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un experto redactor para redes sociales."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, ValueError) as e:
            raise Exception(f"Invalid JSON structure in response: {response.text}") from e
    else:
        return f"Error: {response.status_code} - {response.text}"
