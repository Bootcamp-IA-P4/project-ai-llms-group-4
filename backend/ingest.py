import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from pathlib import Path

# Cargar variables de entorno si necesitas usar alguna
load_dotenv()

# 1. Cargar el documento
doc_path = Path(__file__).resolve().parents[1] / "data" / "ruiztech_info.md"
loader = TextLoader(str(doc_path), encoding="utf-8")
documents = loader.load()

# 2. Dividir en chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = splitter.split_documents(documents)

# 3. Convertir texto en vectores
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Crear base vectorial y guardar localmente
db = FAISS.from_documents(texts, embeddings)
db.save_local("faiss_index")

print("✅ Índice FAISS creado y guardado.")
