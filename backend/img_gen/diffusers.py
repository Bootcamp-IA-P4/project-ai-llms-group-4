from .models import ImagePrompt
from .utils import image_output
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import argparse
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import torch
import os
import time

pipe = None
output_dir = "output"
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

# Loads the Stable Diffusion model if not already loaded.
def load():
    try:
        global pipe
        if pipe is None:
            print("Loading model... at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # Check if CUDA(GPU) is available and set the device accordingly
            device = "cuda" if torch.cuda.is_available() else "cpu"
            pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
            pipe = pipe.to(device)
            print(f"Model loaded on {device}. Finished loading at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        else:
            print("Model already loaded.")
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)



# Generates an image based on the provided ImagePrompt and the Stable Diffusion model.
def main(img = default_image_prompt, output_path=output_path):
    # Load the Stable Diffusion model
    load()
    # Generate the image based on the provided ImagePrompt
    prompt = img.to_prompt() if isinstance(img, ImagePrompt) else "Generate an image for this text " + img
    image = pipe(prompt).images[0]

    return image_output(image,output_path)

    

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

    # Parse the image prompt string into an ImagePrompt object
    img_prompt = parse_image_prompt(args.img_prompt) if args.img_prompt else default_image_prompt

    # Generate the image based on the provided prompt and save it
    print("Generating image with the following parameters:")
    print(f"Image Prompt: {img_prompt}")
    print(f"Output Path: {args.path}")
    main(img_prompt, args.path)