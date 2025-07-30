from datetime import datetime
from backend.database.supabase_client import get_supabase_client

def log_post_to_supabase(data: dict):
    client = get_supabase_client()

    payload = {
        "prompt_input": data.get("prompt"),
        "generated_text": data.get("text"),
        "platform": data.get("platform"),
        "tone": data.get("tone"),
        "language": data.get("language"),
        "audience": data.get("audience"),
        "company": data.get("company"),
        "model_used": data.get("model"),
        "image_url": data.get("image_url"),
        "doc_url": data.get("doc_url"),
        "created_at": datetime.utcnow().isoformat()
    }
    
    print("📝 Payload a insertar en Supabase:")
    for k, v in payload.items():
        print(f"{k}: {v}")

    try:
        response = client.table("posts_history").insert(payload).execute()
        print("✅ Post guardado en Supabase")
        return True
    except Exception as e:
        print(f"❌ Error al guardar en Supabase: {e}")
        return False
