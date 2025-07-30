import os
import requests
import feedparser
import fitz  # PyMuPDF
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
from tempfile import gettempdir
from urllib.parse import quote_plus
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el modelo de embeddings que convertirá texto en vectores numéricos
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Pinecone index config (debe existir en la nube)
PINECONE_INDEX = "generated-posts"   
API_KEY = os.getenv("PINECONE_API_KEY")
ENVIRONMENT = os.getenv("PINECONE_ENV")

# Creamos la conexión al vector store de Pinecone usando el modelo de embeddings
vector_db = PineconeVectorStore.from_existing_index(
    index_name=PINECONE_INDEX,
    embedding=embedding_model
)


def search_arxiv(topic: str, max_results: int = 3):
    encoded_topic = quote_plus(topic)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_topic}&start=0&max_results={max_results}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("❌ Error al consultar arXiv")

    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries:
        pdf_url = next((l.href for l in entry.links if l.type == "application/pdf"), None)
        if pdf_url:
            results.append({
                "title": entry.title,
                "pdf_url": pdf_url,
                "id": entry.id.split("/")[-1],
            })
    return results


def download_and_extract(pdf_url: str, paper_id: str) -> Tuple[str, str]:
    pdf_path = os.path.join(gettempdir(), f"{paper_id}.pdf")

    r = requests.get(pdf_url)
    with open(pdf_path, "wb") as f:
        f.write(r.content)

    doc = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in doc])
    doc.close()

    try:
        os.remove(pdf_path)
    except Exception as e:
        print(f"⚠️ No se pudo borrar el archivo temporal: {e}")

    return full_text, paper_id


# 🧠 Ingestar texto en Pinecone
def ingest_arxiv_documents(docs: List[Tuple[str, str]]):
    documents = [Document(page_content=text, metadata={"source": source}) for text, source in docs]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    vector_db.add_documents(chunks)
    print(f"✅ Ingestados {len(chunks)} fragmentos a Pinecone")


# 🔁 Crear cadena RAG con retriever y LLM
def create_arxiv_rag_chain():
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.7,
        max_tokens=500
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
    Responde a la siguiente pregunta con base en los documentos científicos proporcionados.
    Usa un lenguaje claro y sencillo para que una persona sin conocimientos técnicos pueda entenderlo.

    Pregunta: {question}

    Contexto: {context}

    Respuesta:
    """
        )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )