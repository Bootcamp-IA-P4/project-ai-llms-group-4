from models import ImagePrompt
from utils import image_output
import argparse
import requests
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from env file
import os

default_image_prompt = ImagePrompt(
    subject=os.getenv("IMG_SUBJECT"),
    style=os.getenv("IMG_STYLE"),
    medium=os.getenv("IMG_MEDIUM"),
    lighting=os.getenv("IMG_LIGHTING"),
    color_palette=os.getenv("IMG_COLOR_PALETTE"),
    composition=os.getenv("IMG_COMPOSITION"),
    resolution=os.getenv("IMG_RESOLUTION"),
    contrast=os.getenv("IMG_CONTRAST"),
    mood=os.getenv("IMG_MOOD"),
    details=os.getenv("IMG_DETAILS"),
)

API_KEY = os.getenv("STABILITY_API_KEY")  # Ensure you have set this in your .env file
if not API_KEY and __name__ == "__main__":
    raise ValueError("API_KEY not found. Please set STABILITY_API_KEY in your .env file.")
ENGINE_ID = os.getenv("STABILITY_ENGINE")  
API_HOST = os.getenv("STABILITY_HOST")

def generate_image(prompt: str, output_path: str):
    url = f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    # Get the image in base64 format
    data = response.json()
    b64_image = data["artifacts"][0]["base64"]
    return image_output(b64_image, output_path)
  
    

def main(img = default_image_prompt, output_path = "server/image-gen/output/output.png"):
    prompt = img.to_prompt() if isinstance(img, ImagePrompt) else "Generate an image for this text " + img
    return generate_image(prompt,output_path) 

# Ejemplo de uso
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generte an image using Stability AI's API.")
    parser.add_argument("--img", type=str, default=default_image_prompt.to_prompt(),
                        help="Image prompt in text format.")
    parser.add_argument(
    "--path",
    type=str,
    default="./server/output/output.png",
    help="Path to save the generated image (default: output/output.png)",
    )
    args = parser.parse_args()
    if args.img:
        print("Generando imagen con el prompt:", args.img)
        main(args.img,args.path)
    else:
        print("Generating image with default prompt:", default_image_prompt.to_prompt())
        main()
  








