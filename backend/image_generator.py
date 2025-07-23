import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import base64

# Cargar .env desde la raíz del proyecto
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*", 
}

def generate_image_url(prompt):
    files = {
        'prompt': (None, prompt),
        'output_format': (None, 'png'),
    }

    response = requests.post(API_URL, headers=headers, files=files)

    if response.status_code == 200:
        # Convertir contenido binario a base64
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"
    else:
        print("❌ Error en API Stability:", response.status_code, response.text)
        return None
