from dotenv import load_dotenv 
import os
from server.chatbox.chains.extract_chain import extract_chain
from server.chatbox.chains.generation_chain import generation_chain
from server.chatbox.utils.validate_json import safe_json_loads
import json

load_dotenv()

# Input del usuario
user_text = """
Hola, quiero un post para Twitter que hable sobre cómo la inteligencia artificial puede ayudar a los profesores a ahorrar tiempo. 
Está pensado para docentes de secundaria de habla inglesa y me gustaría que fuera en un tono inspirador. 
Al final pon algo como 'Síguenos para más consejos'.
"""

# Paso 1: extraer información del texto
extracted = extract_chain.invoke({"user_input": user_text})
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
print("\n✅ Generated post:\n", post_result.content)


if __name__ == "__main__":
    # Save the generated post to a file
    with open("generated_post.json", "w") as f:
        json.dump(parsed_data, f, indent=4)
    print("\nGenerated post saved to 'generated_post.json'.")