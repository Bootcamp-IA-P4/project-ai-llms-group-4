from langchain.prompts import PromptTemplate

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
Do not wrap your response in markdown, introduce it with "```json" nor say "Here is the JSON". 
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
