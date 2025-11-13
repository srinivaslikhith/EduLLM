EduLLM: AI Teaching Assistant

This is a RAG (Retrieval-Augmented Generation) Q&A bot that answers questions about your course materials using Google's Gemini AI.

1. Setup

Clone the repository:

git clone [https://github.com/your-username/EduLLM.git](https://github.com/your-username/EduLLM.git)
cd EduLLM


Create and activate a virtual environment:

python3 -m venv env
source env/bin/activate


Install dependencies:

pip install -r requirements.txt


2. Configuration

Create a file named .env in the root folder and add the following, filling in your API key.

# Get from Google AI Studio (aistudio.google.com)
GOOGLE_API_KEY="AIzaSy...Your...Secret...Key"

# --- File Path Configuration ---
DATA_PATH="data/"
DB_FAISS_PATH="faiss_index"
EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"


3. Local Usage

Step 1: Ingest Data (One-Time Setup)

This step creates your local "brain" from your documents.

Create the data folder and add your PDFs to it:

mkdir data
# (Manually add your .pdf files to the 'data' folder)


Run the ingestion script:

python ingest.py


This will create a faiss_index folder.

Step 2: Run the Q&A Bot

Once your faiss_index exists, you can run the bot.

Run the main.py script:

python main.py


Wait for the models to load, then ask questions at the > prompt.

> what is this course about?

Thinking...

--- Answer ---
Based on the provided materials, this course is an introduction to...
--------------

> exit
