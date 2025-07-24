import os
from PIL import Image
import io
import base64
from langdetect import detect
from deep_translator import GoogleTranslator
from keybert import KeyBERT
import requests
import subprocess

# STRING FUNCTIONS

def detect_and_translate(text: str) -> str:
    text = text.replace("#", "").strip()  # Remove hashtags and extra spaces
    detected_lang = detect(text)
    print(f"🌍 Detected language: {detected_lang}")
    if detected_lang != "en":
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print(f"🌐 Translated text: {translated}")
        return translated
    return text


def extract_keywords(text, top_n=5):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    print(f"🔑 Extracted keywords: {keywords}")
    return [kw for kw, score in keywords]

# IMAGE FUNCTIONS

def Image2Base64(image: Image.Image) -> str:
    """
    Convierte una imagen PIL a una cadena base64.
    """
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        exit(1)

def Base642Image(base64_string: str) -> Image.Image:
    """
    Convierte una cadena base64 a una imagen PIL.
    """
    try:
        image_bytes = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        exit(1)
        
def image_output(image, filepath=None):
    if filepath is None or filepath.strip() == "": # Return data URI
        if isinstance(image, str):
            return f"data:image/png;base64,{image}" 
        else:
            return f"data:image/png;base64,{Image2Base64(image)}" 
        
    elif filepath is not None and filepath.strip() != "": # Save file to outputpah
        save_image(image, filepath)


def save_image(image, filepath):
    try:
        # If image is a string, we assume its base64 representation and convert it to PIL Image
        if isinstance(image, str):
            image = Base642Image(image)

        # Ensure the directory exists
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Check if file already exists and handle accordingly
        base, ext = os.path.splitext(filepath)
        new_filepath = filepath
        counter = 1

        while os.path.exists(new_filepath):
            respuesta = input(f"⚠️ File '{new_filepath}' already exists. Overwrite? (y/n): ").strip().lower()
            if respuesta == 'y':
                break
            else:
                new_filepath = f"{base}_{counter}{ext}"
                counter += 1
        
        image.save(new_filepath)
        print(f"💾 Image saved to {new_filepath}")

    except Exception as e:
        print(f"Error saving image: {e}")
        exit(1)

def download_image_from_url(url, output_path="output/output.jpg"):
    img_data = requests.get(url).content
    # with open(filename, "wb") as handler:
    #     handler.write(img_data)
    save_image(Image.open(io.BytesIO(img_data)), output_path)

def get_image_base64_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        base64_image = base64.b64encode(response.content).decode('utf-8')
        return f"data:image/png;base64,{base64_image}"
    else:
        raise Exception(f"Error al descargar imagen: {response.status_code}")

# OLLAMA FUNCTIONS

def is_ollama_installed():
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, check=True)
        print(f"Ollama installed. Version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Ollama is not installed. Please install it from https://ollama.com/docs/installation.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error trying to run Ollama: {e}")
        return False


