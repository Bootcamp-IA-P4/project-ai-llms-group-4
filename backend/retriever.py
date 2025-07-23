from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def get_relevant_chunks(query: str, k: int = 3) -> list[str]:
    """
    Recupera los k fragmentos más relevantes del índice FAISS para una consulta dada.

    Args:
        query (str): Consulta o tema a buscar.
        k (int): Número de fragmentos que se quieren recuperar.

    Returns:
        List[str]: Lista de textos relevantes como strings.
    """

    # Cargar modelo de embedding
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Cargar índice FAISS previamente guardado
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Buscar los fragmentos más relevantes para la consulta
    docs: list[Document] = db.similarity_search(query, k=k)

    # Extraer el contenido textual de los documentos encontrados
    return [doc.page_content for doc in docs]
