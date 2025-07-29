import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from .generate_with_rag import generate_text_with_context
from .image_generator import generate_image_url
from backend.financial.models import FinancialNewsRequest
from backend.financial.financial_service import generate_financial_news
from backend.vector_db.db_manager import save_post, search_similar, ingest_document
from backend.agents.agent import image_agent
from fastapi import Body
from backend.cience_data.arxiv import search_arxiv, download_and_extract, ingest_arxiv_documents, create_arxiv_rag_chain
from backend.database.supabase_logger import log_post_to_supabase
from backend.database.storage import upload_image_to_supabase

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
    img_model: Optional[str] = "stability"
    model_writer: str 
    model_research: Optional[str] = None
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

class ArxivIngestRequest(BaseModel):
    topic: str
    max_papers: Optional[int] = 3

class ArxivQueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "✅ API en funcionamiento"}

# @app.post("/generate")
# def generate_content(data: ContentRequest):
#     """
#     1️⃣ Genera el texto y el prompt usado.
#     2️⃣ (Opcional) Genera imagen usando el texto generado como prompt.
#     3️⃣ Guarda todo en la base vectorial.
#     4️⃣ Devuelve los resultados al frontend.
#     """
#     # 1️⃣ Generar texto y prompt real
#     text, prompt_used = generate_text_with_context(
#         topic=data.topic,
#         platform=data.platform,
#         company=data.company,
#         tone=data.tone,
#         language=data.language,
#         model=data.model,
#         img_model=data.img_model,
#         audience=data.audience
#     )
#     # 2️⃣ (Opcional) Generar imagen
#     image_url = None
#     if data.generate_image:
#         # Solo pasamos el texto generado
#         image_url = image_agent(text, data.img_model)

#     # 3️⃣ Guardar en Pinecone (vectorial)
#     save_post(
#         text=text,
#         prompt=prompt_used,
#         platform=data.platform,
#         tone=data.tone,
#         company=data.company,
#         language=data.language,
#         audience=data.audience,
#         model=data.model,
#         image_url=image_url
#     )

#     # 4️⃣ Devolver al frontend
#     return {
#         "text": text,
#         "image": image_url
#     }

@app.post("/generate")
def generate_content(data: ContentRequest):
    """
    1️⃣ Genera texto e imagen (opcional).
    2️⃣ Sube imagen a Supabase Storage (si existe).
    3️⃣ Guarda en Pinecone (vectorial).
    4️⃣ Guarda en Supabase (relacional).
    5️⃣ Devuelve respuesta.
    """
    # Fallback: si no se proporciona model_research, usa el mismo que model_writer
    model_research = data.model_research or data.model_writer

    # 1️⃣ Generar texto y prompt real
    text, prompt_used = generate_text_with_context(
        topic=data.topic,
        platform=data.platform,
        company=data.company,
        tone=data.tone,
        language=data.language,
        model_writer=data.model_writer,
        model_research=model_research,
        img_model=data.img_model,
        audience=data.audience
    )


    # 2️⃣ (Opcional) Generar imagen
    image_url = None
    if data.generate_image:
        image_url = image_agent(text, data.img_model)

    # 3️⃣ Guardar en Pinecone (vectorial)
        # 2️⃣ (Opcional) Generar imagen
    image_url = None
    if data.generate_image:
        image_path = generate_image_url(text, data.img_model)
        if image_path and os.path.exists(image_path):
            uploaded_url = upload_image_to_supabase(image_path)
            if uploaded_url and uploaded_url.startswith("http"):
                image_url = uploaded_url
                try:
                    os.remove(image_path)
                except Exception as del_err:
                    print(f"⚠️ No se pudo eliminar imagen local: {del_err}")
            else:
                print("⚠️ La imagen no se subió correctamente")
        else:
            print("⚠️ No se generó imagen válida")

    # 4️⃣ Guardar en Pinecone (vectorial)
    save_post(
        text=text,
        prompt=prompt_used,
        platform=data.platform,
        tone=data.tone,
        company=data.company,
        language=data.language,
        audience=data.audience,
        model=data.model_writer,
        image_url=image_url
    )

    # 4️⃣ Devolver resultado
    # 5️⃣ Guardar en Supabase (relacional)
    log_post_to_supabase({
        "prompt": prompt_used,
        "text": text,
        "platform": data.platform,
        "tone": data.tone,
        "company": data.company,
        "language": data.language,
        "audience": data.audience,
        "model": data.model,
        "image_url": image_url
    })

    # 6️⃣ Devolver al frontend
    return {
        "text": text,
        "image_url": image_url
    }


# Endpoint para crear noticias financieras
@app.post("/financial-news")
def financial_news_endpoint(data: FinancialNewsRequest):
    """
    - Recibe: topic, company, language
    - Devuelve: noticia financiera profesional con datos actualizados para la empresa específica
    """
    return generate_financial_news(data)

# Endpoint para obtener noticias financieras
@app.get("/financial-news")
def get_financial_news_endpoint(limit: int = 10):
    """
    - Obtiene: noticias financieras recientes con fechas en español
    - Parámetros: limit (opcional, default=10)
    - Devuelve: lista de noticias ordenadas por fecha
    """
    from backend.database.repository import get_recent_financial_news
    return get_recent_financial_news(limit)

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


@app.post("/arxiv_ingest")
def arxiv_ingest(data: ArxivIngestRequest):
    papers = search_arxiv(data.topic, max_results=data.max_papers)
    if not papers:
        return {"message": "No se encontraron papers."}
    
    docs = []
    for paper in papers:
        try:
            text, source = download_and_extract(paper["pdf_url"], paper["id"])
            docs.append((text, source))
        except Exception as e:
            print(f"❌ Error con {paper['title']}: {e}")

    ingest_arxiv_documents(docs)
    return {"message": f"{len(docs)} papers indexados correctamente."}



@app.post("/arxiv_query")
def arxiv_query(data: ArxivQueryRequest):
    rag = create_arxiv_rag_chain()
    answer = rag.run(data.question)
    return {"question": data.question, "answer": answer}