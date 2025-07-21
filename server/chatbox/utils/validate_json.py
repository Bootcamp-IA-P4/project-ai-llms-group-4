import json

def safe_json_loads(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ Error: El modelo no devolvió un JSON válido")
        return {}
