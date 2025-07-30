import requests
import os
import argparse
from dotenv import load_dotenv
from models import ImagePrompt
from utils import extract_keywords, download_image_from_url, get_image_base64_from_url

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if (not PEXELS_API_KEY or PEXELS_API_KEY == "") and __name__ == "__main__":
    raise ValueError("PEXELS_API_KEY environment variable is not set.")

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

output_path = "server/image-gen/output/output.png"

def search_pexels_by_keywords(keywords):
    try:
        query = " ".join(keywords[:3])  # combinar palabras clave
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json()
            if results["photos"]:
                return results["photos"][0]["src"]["large"]
            else:
                print("No images found for the given keywords.")
                return None
        else:
            raise Exception(f"Pexels API error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error searching Pexels: {e}")
        return None

def main(img=default_image_prompt, output_path="server/image-gen/output/output.png"):
    image_url = search_pexels_by_keywords(
        extract_keywords(img.to_prompt() if isinstance(img, ImagePrompt) else img, top_n=5)
    )
    if output_path:
        download_image_from_url(image_url, output_path)
        return output_path
    else:
        return get_image_base64_from_url(image_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using Pexels API.")
    parser.add_argument(
        "--path",
        type=str,
        default=output_path,
        help="Path to save the generated image (default: output/output.png)",
    )
    parser.add_argument(
        "--img_prompt",
        type=str,
        default=None,
        help="ImagePrompt as a string for image generation (default: env-based prompt)",
    )
    args = parser.parse_args()

    main(
        img=args.img_prompt if args.img_prompt else default_image_prompt,
        output_path=args.path
    )
