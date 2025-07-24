import argparse
import os
from dotenv import load_dotenv
load_dotenv()
from .models import ImagePrompt
from .utils import detect_and_translate
from .diffusers import main as diffusers_prompt
from .stability import main as stability_prompt

pipe = None
output_dir = "server/img-gen/output"
output_filename = "output.png"
output_path = os.path.join(output_dir, output_filename)

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

def generate_post_image(prompt, model, output_path: str = output_path):
    if not isinstance(prompt, ImagePrompt):
        prompt = detect_and_translate(prompt)
    elif isinstance(prompt, ImagePrompt):
         for key, value in prompt.__dict__.items():
            value = detect_and_translate(value) if value != "" and value is not None else ""
    if model == "local":
            print("Generating image using local model...") # Debugging statement
            return diffusers_prompt(prompt, output_path) # Generate image using local model
    elif model == "stability":
            print("Generating image using Stability AI model...") # Debugging statement
            resultado = stability_prompt(prompt, output_path) # Generate image using Stability AI model API
            print(resultado)
            return resultado
    else:
        raise ValueError(f"Invalid model: {model}. Choose 'local' or 'stability'.")


if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description="Generate images using Stable Diffusion.")
    parser.add_argument(
        "--path",
        type=str,
        default="",
        help="Path to save the generated image (default: output/output.png)",
    )
    parser.add_argument(
        "--img_prompt",
        type=str,
        default=default_image_prompt,
        help="User ImagePrompt for image generation (default: default_image_prompt)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["local", "stability"],
        default="stability",
        help="Model to use for image generation (default: local)",
    )
    args = parser.parse_args()

    # Detect language and translate if necessary
    try:
         prompt = detect_and_translate(args.img_prompt)  
    except Exception as e:
        print(f"Error detecting or translating prompt: {e}")

    # Generate image using the specified model
    try:
        generate_post_image(prompt = prompt, model = args.model, output_path = args.path)
    except Exception as e:
        print(f"Error generating image: {e}")
