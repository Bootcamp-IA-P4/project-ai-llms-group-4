import requests
import os
import argparse
from dotenv import load_dotenv
from .models import ImagePrompt
from .utils import extract_keywords, download_image_from_url, get_image_base64_from_url

load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
if (not UNSPLASH_ACCESS_KEY or UNSPLASH_ACCESS_KEY == "") and __name__ == "__main__":
    raise ValueError("UNSPLASH_ACCESS_KEY environment variable is not set.")

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

def search_unsplash_by_keywords(keywords):
    try:
        query = ",".join(keywords[:3])  # combinar palabras clave
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json()
            if results["results"]:
                return results["results"][0]["urls"]["regular"]
            else:
                print("No images found for the given keywords.")
                return None
        else:
            raise Exception(f"Unsplash API error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error searching Unsplash: {e}")
        return None

def main(img = default_image_prompt, output_path = "server/image-gen/output/output.png"):
    unsplash_img  = search_unsplash_by_keywords(extract_keywords(img.to_prompt() if isinstance(img, ImagePrompt) else img, top_n=5))
    if output_path and output_path.strip() != "":
        download_image_from_url(unsplash_img, output_path)
        return output_path
    else:
     return get_image_base64_from_url(unsplash_img)


if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description="Generate images using Stable Diffusion.")
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
        help="User ImagePrompt as a string for image generation (default: environment-based default_image_prompt)",
    )
    args = parser.parse_args()


    main(img=args.img_prompt if args.img_prompt else default_image_prompt, output_path=args.path)