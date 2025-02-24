# Proje klasör yapısı
rag_project
│── docker-compose.yml
│── ollama_data/ (Model dosyaları için)
│── chroma_data/ (Veri tabanı için)
│── scripts/
│   ├── ingest_documents.py  (Dokümanları içeri aktaran Python kodu)
│   ├── query_model.py       (Modele soru soran Python kodu)
│── documents/ (Şirket dokümanları)
│   ├── policy.pdf
│   ├── backup.xlsx
│   ├── security.docx

# Ollama modelini indir
ollama pull deepseek/deepseek-r1

# Docker Compose ile servisleri başlat
docker compose up -d

# Yukarıdaki scriptleri çalıştırmadan önce, Docker içinde Python ortamı açalım.
docker run --rm -it -v $(pwd):/app -w /app python:3.10 bash
pip install langchain chromadb pypdf python-docx pandas openpyxl requests

# Her gün dökümanları güncelleyip tekrar indekslemek için Linux cronjob ekleyebilirsin
crontab -e

0 3 * * * /usr/bin/python3 /path/to/ingest_documents.py
