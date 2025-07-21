from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json

# Inicialización del modelo LLM
llm = Ollama(
    model="gemma3",
    temperature=0.7,
)

# Prompt para extraer información del texto del usuario
extract_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are an assistant that extracts structured information from user requests.

Extract the following fields:
- Topic
- Audience
- Platform
- Style
- Call to Action
- Language
- Product
- Brand
- Company

Only respond with a valid **single-line JSON object**.
Do not explain anything.
Do not wrap your response in markdown, introduce it with "```json" nor introduce it with or say "Here is the JSON". 
Do not include any additional text or comments.
Just return the JSON object with the extracted information.
Remember the output must start and end with curly braces, not ``` marks and must be a valid JSON object.

User input:
{user_input}

Example:
{{
  "topic": "...",
  "audience": "...",
  "platform": "...",
  "style": "...",
  "call_to_action": "...",
  "language": "...",
  "brand": "...",
  "company": "...",
  "product": "..."
}}

Make sure to include all fields, even if they are empty. If a field is not applicable, leave it as an empty string.

"""
)

# Prompt para generar el contenido con la información extraída
generation_prompt = PromptTemplate(
    input_variables=["topic", "audience", "platform", "style", "call_to_action", "language", "brand", "company", "product"],
    template="""
You are a professional copywriter and social media strategist.
Create a {platform} post about "{topic}" targeted at {audience} in {language} language.
The post should also mention the {brand} and {company} of any {product} or service related to the topic.
Use a {style} tone.
Include a strong call-to-action: {call_to_action}.

Make it engaging, authentic, and optimized for the platform.
"""
)



# Chain para extraer datos
extract_chain = LLMChain(
    llm=llm,
    prompt=extract_prompt,
    output_key="extracted_json"
)

# Chain para generar el contenido
generation_chain = LLMChain(
    llm=llm,
    prompt=generation_prompt,
    output_key="generated_post"
)

# Input libre del usuario
user_text = """
Hola, quiero un post para Twitter que hable sobre cómo la inteligencia artificial puede ayudar a los profesores a ahorrar tiempo. 
Está pensado para docentes de secundaria de habla inglesa y me gustaría que fuera en un tono inspirador. 
Al final pon algo como 'Síguenos para más consejos'.
"""

# Paso 1: extraer información del texto del usuario
result = extract_chain.invoke({"user_input": user_text})
extracted = result["extracted_json"]

print("🧪 Extracted output:\n", extracted)


# Paso 2: convertir el JSON a diccionario
try:
    parsed_data = json.loads(extracted)
except json.JSONDecodeError:
    print("❌ Error: El modelo no devolvió un JSON válido")
    exit(1)

# Validación básica por si alguna clave está vacía
defaults = {
    "brand": "your brand",
    "company": "your company",
    "product": "your product",
    "call_to_action": "Follow us for more!"
}
for key, value in defaults.items():
    if not parsed_data.get(key):
        parsed_data[key] = value

# Paso 3: generar el contenido usando los datos extraídos
post_result = generation_chain.invoke(parsed_data)

# Mostrar resultado

print("\n✅ Generated post:\n", post_result["generated_post"])
