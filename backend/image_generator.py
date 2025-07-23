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

<<<<<<< HEAD:app/image_generator.py
def generate_image_url(topic, platform=None, tone=None, audience=None, size="1024x1024", style="photographic"):
    """
    Generate an image based on topic and optional parameters.
    
    Args:
        topic (str): Main topic for the image
        platform (str, optional): Social media platform 
        tone (str, optional): Tone of the content
        audience (str, optional): Target audience
        size (str, optional): Image size (e.g., "1024x1024")
        style (str, optional): Image style (e.g., "photographic", "illustration")
        
    Returns:
        str: Base64 encoded image data URL or None if failed
    """
    # Create a more detailed prompt based on parameters
    if platform or tone or audience:
        detailed_prompt = f"{topic}"
        if platform:
            detailed_prompt += f" for {platform}"
        if audience:
            detailed_prompt += f", targeting {audience}"
        if tone:
            detailed_prompt += f", in a {tone.lower()} tone"
        prompt = detailed_prompt
    else:
        prompt = topic
    
    # Add style description to the prompt
    style_descriptions = {
        "photographic": "photorealistic, high-quality photograph",
        "illustration": "digital illustration, vibrant colors",
        "3d": "3D rendered image, with depth and texture",
        "cartoon": "cartoon style, vibrant and stylized"
    }
    
    style_desc = style_descriptions.get(style, "photorealistic")
    prompt = f"{prompt}, {style_desc}"
    
=======
def generate_image_url(text):
    """
    Genera una imagen usando el texto generado por el LLM.
    """
>>>>>>> origin/dev:backend/image_generator.py
    files = {
        'prompt': (None, text),  # Aquí el texto del post generado
        'output_format': (None, 'png'),
        'dimensions': (None, size),
    }

    response = requests.post(API_URL, headers=headers, files=files)

    if response.status_code == 200:
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"
    else:
        print("❌ Error en API Stability:", response.status_code, response.text)
        return None
