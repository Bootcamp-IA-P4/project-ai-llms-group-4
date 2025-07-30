# backend/vector_db/document_reader.py

import os

# Librerías específicas para cada tipo de documento
import fitz  # PyMuPDF para PDFs
import docx  # python-docx para archivos Word
import markdown

def extract_text_from_file(file_path: str) -> str:
    """
    Extrae el texto de un archivo según su extensión (.txt, .pdf, .docx, .md).
    Devuelve el contenido como string.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return _read_txt(file_path)
    elif ext == ".pdf":
        return _read_pdf(file_path)
    elif ext == ".docx":
        return _read_docx(file_path)
    elif ext == ".md":
        return _read_markdown(file_path)
    else:
        raise ValueError(f"❌ Tipo de archivo no soportado: {ext}")

# Funciones privadas para cada tipo
def _read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def _read_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def _read_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def _read_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_md = f.read()
    return markdown.markdown(raw_md)  # Puedes usar raw_md si prefieres texto plano
