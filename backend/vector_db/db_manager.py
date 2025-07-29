import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from .document_reader import extract_text_from_file

# Cargamos las variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# Inicializamos el modelo de embeddings que convertirá texto en vectores numéricos
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Pinecone index config (debe existir en la nube)
INDEX_NAME = "generated-posts"   
API_KEY = os.getenv("PINECONE_API_KEY")
ENVIRONMENT = os.getenv("PINECONE_ENV")

# Creamos la conexión al vector store de Pinecone usando el modelo de embeddings
vector_db = PineconeVectorStore.from_existing_index(
    index_name=INDEX_NAME,
    embedding=embedding_model
)


def save_post(
    text,
    prompt,
    platform,
    tone,
    company=None,
    language=None,
    audience=None,
    model=None,
    image_url=None
):
    metadata = {
        "prompt": prompt,
        "platform": platform,
        "company": company,
        "tone": tone,
        "language": language,
        "audience": audience,
        "model": model,
        "image_url": image_url
    }
    # Filtra claves con valor None (Pinecone no acepta None)
    metadata_clean = {k: v for k, v in metadata.items() if v is not None}
    vector_db.add_texts([text], metadatas=[metadata_clean])
    print("✅ Post guardado en Pinecone con metadatos:", metadata_clean)


def search_similar(query, top_k=3):
    """
    Busca los posts más similares semánticamente al query recibido.
    Devuelve tuplas (documento, score de similitud).
    """
    results = vector_db.similarity_search_with_score(query, k=top_k)
    return results

def ingest_document(file_path: str, source_name: str = None):
    """
    Dividimos el documento en fragmentos y los guardamos en Pinecone con metadatos.
    - file_path: Ruta al archivo de texto a procesar
    - source_name: Nombre identificador del documento (opcional)
    """
        # 1. Lee el documento
    
    content = extract_text_from_file(file_path)


        # 2. Divide en chunks para mejorar la búsqueda semántica
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(content)

        # 3. Sube cada fragmento a Pinecone con metadatos (incluye el nombre del documento original)
    metadatas = [{"source": source_name or file_path}] * len(chunks)
    vector_db.add_texts(chunks, metadatas=metadatas)
    print(f"✅ Documento '{file_path}' indexado en Pinecone ({len(chunks)} fragmentos)")

# Este bloque permite usar el archivo como script para pruebas directas desde consola
if __name__ == "__main__":
     # Prueba: guardar un post de ejemplo
    save_post(
        text="Tips for creating viral content on Instagram.",
        prompt="Generate tips for viral Instagram posts.",
        platform="Instagram",
        tone="Creative",
        company="RuizTech",
        language="English",
        audience="Millennials",
        model="mistralai/mistral-7b-instruct",
        image_url="https://fakeurl.com/image.png"
    )

    print("\n🔍 Resultados de búsqueda por similitud:")
    results = search_similar("Ideas for Instagram posts", top_k=2)
    for doc, score in results:
        print(f"\n---\nScore: {score:.3f}")
        print("Text:", doc.page_content)
        print("Metadata:", doc.metadata)

   
