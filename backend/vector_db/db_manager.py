import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Cargamos las variables de entorno necesarias para Pinecone
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# 2. Inicializamos el cliente de Pinecone usando nuestra API Key y entorno
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# 3. Seleccionamos el modelo de embeddings (nos aseguramos de que la dimensión coincide con la del índice en Pinecone)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Especificamos el nombre EXACTO de tu índice en Pinecone
INDEX_NAME = "generated-posts"
ENVIRONMENT = os.getenv("PINECONE_ENV")
# 5. Conectamos con el índice de Pinecone usando LangChain
vector_db = PineconeVectorStore.from_existing_index(
    INDEX_NAME,
    embedding_model,
    pool_kwargs={
        "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
        "environment": ENVIRONMENT,
    }
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
    # Añadimos el texto (embedding) y sus metadatos al vector DB
    vector_db.add_texts([text], metadatas=[metadata])
    print("✅ Post guardado en Pinecone con metadatos:", metadata)

def search_similar(query, top_k=3):
    """
    Busca los posts más similares semánticamente al query recibido.
    Devuelve tuplas (documento, score de similitud).
    """
    results = vector_db.similarity_search_with_score(query, k=top_k)
    return results

if __name__ == "__main__":
    # Ejemplo: guardar un post de prueba
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
