import os
from pathlib import Path
from backend.database.supabase_client import get_supabase_client

def upload_image_to_supabase(local_path: str, bucket_name="posts") -> str:
    """
    Sube una imagen a Supabase Storage y devuelve la URL pública.
    Si falla, devuelve None.
    """
    client = get_supabase_client()
    file_name = Path(local_path).name
    storage_path = f"{bucket_name}/{file_name}"

    try:
        # Subir el archivo al bucket especificado
        with open(local_path, "rb") as f:
            res = client.storage.from_(bucket_name).upload(storage_path, f, {"upsert": True})

        # Obtener la URL pública
        public_url = client.storage.from_(bucket_name).get_public_url(storage_path)
        return public_url

    except Exception as e:
        print(f"❌ Error subiendo imagen a Supabase Storage: {e}")
        return None
