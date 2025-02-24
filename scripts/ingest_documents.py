import os
import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document
import fitz  # PyMuPDF
import pandas as pd

# Klasör yolu
DOCS_PATH = "./documents"

# ChromaDB istemcisi
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection(name="company_docs")

# Metin bölücü
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Dosya okuma fonksiyonları
def load_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

def load_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_xlsx(file_path):
    df = pd.read_excel(file_path, sheet_name=None)
    return "\n".join([df[sheet].to_string(index=False) for sheet in df])

# Dokümanları yükleme
documents = []
for filename in os.listdir(DOCS_PATH):
    file_path = os.path.join(DOCS_PATH, filename)
    if filename.endswith(".pdf"):
        documents.append((filename, load_pdf(file_path)))
    elif filename.endswith(".docx"):
        documents.append((filename, load_docx(file_path)))
    elif filename.endswith(".xlsx"):
        documents.append((filename, load_xlsx(file_path)))

# ChromaDB'ye ekleme
for filename, text in documents:
    chunks = text_splitter.split_text(text)
    for chunk in chunks:
        collection.add(documents=[chunk], ids=[filename + str(hash(chunk))])

print("Dokümanlar başarıyla yüklendi!")
