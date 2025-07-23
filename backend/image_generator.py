import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import base64
from backend.img_gen.main import generate_post_image

# Cargar .env desde la raíz del proyecto
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*", 
}

def generate_image_url(text):
    """
    Genera una imagen usando el texto generado por el LLM.
    """
    try:
        print("Calling generate_post_image def...")
        return generate_post_image(text[:2000], "stability", None)       
    except Exception as e:
        print("Error retrieving image from model:", e)
        return None 