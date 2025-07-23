import os
from PIL import Image
import io
import base64

def save_image(image, filepath):
    try:
        # Si image es un string, asumimos que es base64
        if isinstance(image, str):
            # Decodificar base64 a bytes
            image_bytes = base64.b64decode(image)
            # Crear BytesIO y abrir con PIL
            image = Image.open(io.BytesIO(image_bytes))

        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

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
