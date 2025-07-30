import os
from pathlib import Path
from database.supabase_client import get_supabase_client

def upload_image_to_supabase(local_path: str, bucket_name="posts") -> str:
    """
    Sube una imagen a Supabase Storage y devuelve la URL pública.
    Si falla, devuelve None.
    """
    client = get_supabase_client()
    file_name = Path(local_path).name
    storage_path = file_name 

    try:
        with open(local_path, "rb") as f:
            print(f"📤 Subiendo imagen '{file_name}' a bucket '{bucket_name}'...")
            res = client.storage.from_(bucket_name).upload(storage_path, f, {"upsert": "true"})

        public_url = client.storage.from_(bucket_name).get_public_url(storage_path)
        print(f"🌐 URL pública generada: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ Error subiendo imagen a Supabase: {e}")
        return None

def upload_document_to_supabase(local_path: str, bucket_name="documents") -> str:
    """
    Sube un documento a Supabase Storage y devuelve la URL pública.
    Si falla, devuelve None.
    """
    client = get_supabase_client()
    file_name = Path(local_path).name
    storage_path = file_name

    try:
        with open(local_path, "rb") as f:
            print(f"📤 Subiendo documento '{file_name}' a bucket '{bucket_name}'...")
            res = client.storage.from_(bucket_name).upload(storage_path, f, {"upsert": "true"})

        public_url = client.storage.from_(bucket_name).get_public_url(storage_path)
        print(f"🌐 URL pública del documento: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ Error subiendo documento a Supabase: {e}")
        return None
