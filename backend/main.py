import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from generate_with_rag import generate_text_with_context
from image_generator import generate_image_url
from financial.models import FinancialNewsRequest
from financial.financial_service import generate_financial_news
from vector_db.db_manager import save_post, search_similar, ingest_document
from fastapi import Body
from cience_data.arxiv import search_arxiv, download_and_extract, ingest_arxiv_documents, create_arxiv_rag_chain
from vector_db.document_reader import extract_text_from_file
from database.supabase_logger import log_post_to_supabase
from database.storage import upload_image_to_supabase
from database.storage import upload_document_to_supabase
from database.supabase_logger import log_post_to_supabase
from database.storage import upload_image_to_supabase

app = FastAPI()

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class ContentRequest(BaseModel):
    topic: str
    platform: str
    company: Optional[str] = None
    tone: str
    language: str
    model_writer: str 
    model_research: Optional[str] = None
    audience: Optional[str] = None
    img_model: Optional[str] = "remote:all"
    generate_image: bool = True

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

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

@app.post("/generate")
def generate_content(data: ContentRequest):
    """
    1️⃣ Genera el texto y el prompt usado.
    2️⃣ (Opcional) Genera imagen usando el texto generado como prompt.
    3️⃣ Guarda todo en la base vectorial.
    4️⃣ Devuelve los resultados al frontend.
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
        audience=data.audience
    )

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
        "model": data.model_writer,
        "image_url": image_url
    })

    # 6️⃣ Devolver al frontend
    return {
        "text": text,
        "image_url": image_url
    }

@app.post("/financial-news")
def financial_news_endpoint(data: FinancialNewsRequest):
    return generate_financial_news(data)

@app.get("/financial-news")
def get_financial_news_endpoint(limit: int = 10):
    from database.repository import get_recent_financial_news
    return get_recent_financial_news(limit)

@app.post("/search")
def search_content(data: SearchRequest):
    results = search_similar(data.query, top_k=data.top_k)
    output: List[SearchResult] = [
        SearchResult(
            text=doc.page_content,
            metadata=doc.metadata,
            similarity_score=round(score, 3)
        )
        for doc, score in results
    ]
    return {"results": output}

@app.post("/upload_document")
def upload_document(
    topic: str = Form(...),
    platform: str = Form(...),
    tone: str = Form(...),
    language: str = Form(...),
    model: str = Form(...),
    img_model: str = Form("remote:all"),
    audience: str = Form(None),
    company: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    extra_context = ""
    file_url = None

    if file:
        temp_dir = Path("backend/tmp_docs")
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / file.filename
        with open(temp_path, "wb") as f_out:
            f_out.write(file.file.read())

        extra_context = extract_text_from_file(temp_path)
        ingest_document(temp_path, source_name=file.filename)
        file_url = upload_document_to_supabase(temp_path)

        if os.path.exists(temp_path):
            os.remove(temp_path)


    text, prompt_used = generate_text_with_context(
        topic=topic,
        platform=platform,
        company=company,
        tone=tone,
        language=language,
        model_writer=model,
        model_research=model,
        img_model=img_model,
        audience=audience,
        extra_context=extra_context
    )

    image_url = None
    if img_model:
        image_path = generate_image_url(text, img_model)
        if image_path and os.path.exists(image_path):
            uploaded_url = upload_image_to_supabase(image_path)
            if uploaded_url and uploaded_url.startswith("http"):
                image_url = uploaded_url
            os.remove(image_path)

    log_post_to_supabase({
        "prompt": prompt_used,
        "text": text,
        "platform": platform,
        "tone": tone,
        "company": company,
        "language": language,
        "audience": audience,
        "model": model,
        "image_url": image_url,
        "doc_url": file_url
    })

    return {
        "text": text,
        "prompt": prompt_used,
        "image": image_url,
        "doc_url": file_url
    }

@app.post("/index_document")
def index_document(file: UploadFile = File(...)):
    allowed_extensions = {".txt", ".pdf", ".docx", ".md"}
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        return {"error": f"❌ Tipo de archivo no permitido: {ext}"}

    temp_dir = Path("backend/tmp_docs")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / file.filename
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    
    try:
        ingest_document(temp_path, source_name=file.filename)
        return {"message": f"✅ Documento {file.filename} indexado correctamente."}
    except Exception as e:
        return {"error": f"❌ Error al procesar el archivo: {str(e)}"}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


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
