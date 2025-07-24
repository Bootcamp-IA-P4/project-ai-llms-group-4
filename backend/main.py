from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from .generate_with_rag import generate_text_with_context
from .image_generator import generate_image_url
from backend.vector_db.db_manager import save_post, search_similar, ingest_document

app = FastAPI()

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class ContentRequest(BaseModel):
    topic: str
    platform: str
    company: Optional[str] = None
    tone: str
    language: str
    audience: Optional[str] = None
    model: str
    generate_image: bool = True

    # Modelo de entrada para búsqueda
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

# Modelo de resultado de búsqueda (opcional, mejora tipado/documentación)
class SearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    similarity_score: float

@app.get("/")
def read_root():
    return {"message": "✅ API en funcionamiento"}

@app.post("/generate")
def generate_content(data: ContentRequest):
    """
    1️⃣ Genera el texto y el prompt usado.
    2️⃣ (Opcional) Genera imagen usando el texto generado como prompt.
    3️⃣ Guarda todo en la base vectorial.
    4️⃣ Devuelve los resultados al frontend.
    """
    # 1️⃣ Generar texto y prompt real
    text, prompt_used = generate_text_with_context(
        topic=data.topic,
        platform=data.platform,
        company=data.company,
        tone=data.tone,
        language=data.language,
        model=data.model,
        audience=data.audience
    )
    # 2️⃣ (Opcional) Generar imagen
    image_url = None
    if data.generate_image:
        image_url = generate_image_url(text)

    # 3️⃣ Guardar en Pinecone (vectorial)
    save_post(
        text=text,
        prompt=prompt_used,
        platform=data.platform,
        tone=data.tone,
        company=data.company,
        language=data.language,
        audience=data.audience,
        model=data.model,
        image_url=image_url
    )

    # 4️⃣ Devolver al frontend
    return {
        "text": text,
        "image": image_url
    }


@app.post("/search")
def search_content(data: SearchRequest):
    """
    Endpoint para buscar posts similares semánticamente en la base de datos vectorial.
    """
    results = search_similar(data.query, top_k=data.top_k)

    output: List[SearchResult] = []
    for doc, score in results:
        output.append(SearchResult(
            text=doc.page_content,
            metadata=doc.metadata,
            similarity_score=round(score, 3)
        ))
    return {"results": output}

@app.post("/upload_document")
def upload_document(file: UploadFile = File(...)):
    """
    Sube e indexa un archivo de texto para consultas semánticas.
    """
    temp_path = f"tmp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    ingest_document(temp_path, source_name=file.filename)

    # Limpia el archivo temporal
    os.remove(temp_path)
    return {"message": f"Documento {file.filename} indexado correctamente."}