import os
from PIL import Image
import io
import base64
from langdetect import detect
from deep_translator import GoogleTranslator

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
            return f"data:image/png;base64,{Image2Base64(image).decode('utf-8')}" 
        
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


def detect_and_translate(text: str) -> str:
    detected_lang = detect(text)
    print(f"🌍 Detected language: {detected_lang}")
    if detected_lang != "en":
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print(f"🌐 Translated text: {translated}")
        return translated
    return text
