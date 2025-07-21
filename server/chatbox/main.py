from dotenv import load_dotenv 
import os
import argparse
from server.chatbox.chains.extract_chain import extract_chain
from server.chatbox.chains.generation_chain import generation_chain
from server.chatbox.utils.validate_json import safe_json_loads
import json

load_dotenv()

# User default input text
default_user_text = """
Hola, quiero un post para Twitter que hable sobre cómo la inteligencia artificial puede ayudar a los profesores a ahorrar tiempo. 
Está pensado para docentes de secundaria de habla inglesa y me gustaría que fuera en un tono inspirador. 
Al final pon algo como 'Síguenos para más consejos'.
"""



def main(user_text, verbose=False):
    """
    Main function to run the extraction and generation process.
    """
    if verbose:
        print("Verbose mode is ON")
        print("User input:", user_text)

    # Paso 1: extraer información del texto
    extracted = extract_chain.invoke({"user_input": user_text})
    if verbose:
        print("🧪 Extracted output:\n", extracted.content)


    # Paso 2: convertir la salida a diccionario
    parsed_data = safe_json_loads(extracted.content)

    # Paso 3: completar campos vacíos con valores por defecto
    defaults = {
        "brand": "your brand",
        "company": "your company",
        "product": "your product",
        "call_to_action": "Follow us for more!"
    }
    for key, value in defaults.items():
        if not parsed_data.get(key):
            parsed_data[key] = value

    # Paso 4: generar contenido

    post_result = generation_chain.invoke(parsed_data)
    if verbose :
        print("\n✅ Generated post:\n", post_result.content)
    return post_result.content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_text", type=str, default=default_user_text, help="Texto de entrada del usuario para generar contenido")
    parser.add_argument("--verbose", action="store_true", help="Muestra información detallada de ejecución")
    args = parser.parse_args()

    main(user_text=args.input_text, verbose=args.verbose)