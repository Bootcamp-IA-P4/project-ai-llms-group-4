# Image Generation Service

This module is part of **Project AI LLMS Group 4** and provides an image generation service using advanced AI models.

## Features

- Generates images based on ImagePrompt objects.
- Implements ImagePrompt class(check models.py for supported class attributes).
- Utilizes the Stable Diffusion model for local image generation.
- Utilizes the StabilityAI API for remote image generation (API key required).


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/project-ai-llms-group-4.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Rename `.env.example` to `.env` file in the root directory.
    - Add necessary configurations (e.g., API keys, model paths).

## Usage

1. Start the server:
    Both parameters are optional, if not provided, the default model will be used.
    
    ```bash
    # For local model:
    python -m server.img-gen.main --model=local --path=server/img-gen/output/output.png
    ```
    ```bash
    # For remote model:
    python -m server.img-gen.main --model=stability --path=server/img-gen/output/output.png
    ```
    ```bash
    # If you want to use the default local model, you can run:
    python -m server.img-gen.main 
    ```

2. The file will be saved in the specified path.

