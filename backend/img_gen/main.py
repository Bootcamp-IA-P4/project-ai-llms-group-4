import argparse
import os
from dotenv import load_dotenv
load_dotenv()
from .models import ImagePrompt
from .utils import detect_and_translate, translate_image_prompt, is_ollama_installed, is_ollama_running
from .diffusers import main as diffusers_prompt
from .stability import main as stability_prompt
from .unsplash import main as unsplash_prompt
from .pexels import main as pexels_prompt

pipe = None
output_dir = "backend/img_gen/output"
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
         prompt = translate_image_prompt(prompt).to_prompt()
    print(f"Prompt: {prompt}") # Debugging statement
    print(f"Model: {model}") # Debugging statement
    model_environment, model_name = model.split(":")
    if model_environment == "local":
            print("Generating image using local model...") # Debugging statement
            if not is_ollama_installed():
                raise OSError("Ollama is not installed. Please install Ollama to use the local model.")
            elif not is_ollama_running():
                raise OSError("Ollama is not running. Please start Ollama to use the local model.")
            else:
                return diffusers_prompt(prompt, output_path)
    elif model_environment == "remote":
        if model_name == "all":
            try:
                print("Generating image using remote models...")    # Debugging statement
                print("Generating image using Stability AI model...") # Debugging statement
                return stability_prompt(prompt, output_path) # Generate image using Stability AI model API
            except Exception as e:
                print(f"Error generating image using Stability AI model: {e}") # Debugging statement
                try:
                    print("Generating image using Pexels API...")
                    return pexels_prompt(prompt, output_path)
                except Exception as e:
                    print(f"Error generating image using Pexels API: {e}") # Debugging statement
                    try:
                        print("Generating image using Unsplash API...")
                        return unsplash_prompt(prompt, output_path)
                    except Exception as e:
                        print(f"Error generating image using Unsplash API: {e}") # Debugging statement
                        raise ValueError("Failed to generate image using both Stability AI, Pexels and Unsplash APIs.")
        elif model_name == "unsplash":
            try:
                print("Generating image using Unsplash API...")
                return unsplash_prompt(prompt, output_path)
            except Exception as e:
                print(f"Error generating image using Unsplash API: {e}") # Debugging statement
                raise ValueError("Failed to generate image using Unsplash API.")
        elif model_name == "pexels":
            try:
                print("Generating image using Pexels API...")
                return pexels_prompt(prompt, output_path)
            except Exception as e:
                print(f"Error generating image using Pexels API: {e}")
                raise ValueError("Failed to generate image using Pexels API.")
        elif model_name == "stability":
            try:
                print("Generating image using Stability AI model...")
                return stability_prompt(prompt, output_path) # Generate image using Stability AI model API
            except Exception as e:
                print(f"Error generating image using Stability AI model: {e}")
                raise ValueError("Failed to generate image using Stability AI model.")  
    else:
        raise ValueError(f"Invalid model: {model}. Supported models are 'local:local', 'remote:all', 'remote:unsplash', 'remote:pexels', and 'remote:stability'.")


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
        default=default_image_prompt,
        help="User ImagePrompt for image generation (default: default_image_prompt)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["local:local", "remote:all", "remote:unsplash", "remote:pexels", "remote:stability"],
        default="remote:all",
        help="Model to use for image generation (default: local)",
    )
    args = parser.parse_args()

    if not args.img_prompt or args.img_prompt == "":
        # If no prompt is provided, use the default image prompt
        prompt = detect_and_translate(default_image_prompt.to_prompt)
    else:
        prompt = args.img_prompt


    # Generate image using the specified model
    try:
        generate_post_image(prompt = args.img_prompt, model = args.model, output_path = args.path)
    except Exception as e:
        print(f"Error generating image: {e}")
