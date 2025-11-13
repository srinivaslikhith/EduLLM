# 🧠 EduLLM: AI Teaching Assistant

A simple RAG-based Q&A bot using local embeddings and Google’s Gemini API.

---

## ⚙️ Setup

```bash
# Clone repo
git clone https://github.com/your-username/EduLLM.git
cd EduLLM

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔧 Configuration

Create a `.env` file in the project root:

```bash
# Get key from https://aistudio.google.com
GOOGLE_API_KEY="AIzaSy...YourKey..."

DATA_PATH="data/"
DB_FAISS_PATH="faiss_index"
EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"
```

---

## 💾 Run Locally

### 1. Ingest Data (run once)
Add your PDFs to a `data/` folder, then run:
```bash
python ingest.py
```

### 2. Start the Bot
```bash
python main.py
```
Ask questions at the prompt, type `exit` to quit.

---

## 📁 Structure

```
EduLLM/
├── data/
├── faiss_index/
├── ingest.py
├── main.py
├── requirements.txt
└── .env
```