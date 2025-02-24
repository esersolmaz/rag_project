import requests
import chromadb

# Open WebUI API URL'si
OPENWEBUI_URL = "http://localhost:3000/api/generate"

# ChromaDB istemcisi
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_collection(name="company_docs")

def get_relevant_text(query):
    results = collection.query(query_texts=[query], n_results=3)
    relevant_docs = "\n\n".join(results["documents"][0]) if results["documents"] else "Bilgi bulunamadı."
    return relevant_docs

def ask_model(query):
    context = get_relevant_text(query)
    prompt = f"Şirket dökümanlarına göre, {query} sorusuna detaylı bir cevap ver.\n\n{context}"

    payload = {
        "model": "deepseek-r1",
        "prompt": prompt,
        "max_tokens": 500
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(OPENWEBUI_URL, json=payload, headers=headers)
    
    return response.json().get("response", "Cevap alınamadı.")

# Kullanıcıdan input al
query = input("Sormak istediğiniz soru: ")
answer = ask_model(query)
print("\n📌 Cevap:\n", answer)
