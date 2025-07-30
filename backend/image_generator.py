import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import base64
from img_gen.main import generate_post_image
from pathlib import Path
import time
from langsmith import traceable

# Cargar .env desde la raíz del proyecto
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*", 
}

from pathlib import Path

@traceable(name="Generación de url de imagen")
def generate_image_url(text, model):
    try:
        print("Calling generate_post_image def...")

        BASE_DIR = Path(__file__).resolve().parents[1]
        unique_name = f"img_{int(time.time())}.png" 
        output_path = BASE_DIR / "backend" / "img_gen" / "output" / unique_name
        output_path = str(output_path)

        print(f"📁 Ruta de salida: {output_path}")
        result_path = generate_post_image(text[:2000], model, output_path)
        return result_path
    except Exception as e:
        print("Error retrieving image from model:", e)
        return None


    