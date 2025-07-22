import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore

# Cargamos las variables de entorno
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

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
    """
    Guarda un post generado en Pinecone con todos los metadatos relevantes.
    """
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
    # Convertimos el texto a embedding y lo guarda en el vector DB junto a los metadatos
    vector_db.add_texts([text], metadatas=[metadata])
    print("✅ Post guardado en Pinecone con metadatos:", metadata)

def search_similar(query, top_k=3):
    """
    Busca los posts más similares semánticamente al query recibido.
    Devuelve tuplas (documento, score de similitud).
    """
    results = vector_db.similarity_search_with_score(query, k=top_k)
    return results

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
