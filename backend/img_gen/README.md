# Image Generation Service

This module is part of **Project AI LLMS Group 4** and provides an image generation service using advanced AI models.

## Features

- Generates images based on ImagePrompt objects or straightforward text prompts.
- Implements ImagePrompt class(check models.py for supported class attributes).
- Utilizes the Stable Diffusion model for local image generation.
- Utilizes the StabilityAI API for remote image generation (API key required).


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/project-ai-llms-group-4.git
    ```
    Change to the `img-gen` branch and pull the latest changes:
    ```bash
    git feature/switch img-gen
    git pull
    ```

2. Install dependencies:
    ```bash
    cd project-ai-llms-group-4/server/img-gen
    pip install -r requirements.txt
    ```
3. Ensure you have the required Key for the StabilityAI API (if using remote model).
    - Visit [StabilityAI](https://stability.ai/) to obtain an API key.

4. Set up environment variables:
    - Create a `.env` file in the root directory, if any or add configuration to the existing one.
    - Add necessary environment variables as in the `.env.example` file.




## Usage

1. Start the server:
    Both parameters are optional, if not provided, the default model will be used.
    
    ```bash
    # For local model:
    python -m server.img-gen.main --model=local --path=server/img-gen/output/output.png --img_prompt="An astronaut riding a horse in a futuristic city" --width=512 --height=512 --num_inference_steps=50 --guidance_scale=7.5"
    ```
    ```bash
    # For remote model:
    python -m server.img-gen.main --model=stability --path=server/img-gen/output/output.png --img_prompt="An astronaut riding a horse in a futuristic city" --width=512 --height=512 --num_inference_steps=50 --guidance_scale=7.5
    ```
    ```bash
    # If you want to use the default local model, you can run:
    python -m server.img-gen.main 
    ```

2. The file will be saved in the specified path.

