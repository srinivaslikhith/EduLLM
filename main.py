import os
from dotenv import load_dotenv

# These are the new, correct imports you helped me identify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Imports for our specific components ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DB_FAISS_PATH = os.getenv("DB_FAISS_PATH")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

# lets load gemini model & embedding model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={'device': 'cpu'} # Run on your CPU
)

# load local vector store
vector_store = FAISS.load_local(
    DB_FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

#now lets create a retreiver to use later in the rag chain
retreiver = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 4}
)

# lets create a prompt template for GEMINI AI to answer based on the context we provided
PROMPT_TEMPLATE = """
You are an expert AI Teaching Assistant for this course.
Your goal is to answer the user's question based  on the 
following context provided from the course materials.

If the answer is not found in the context, say:
"I'm sorry, I don't have information on that topic based on the provided materials."

Do not make up an answer or provide information from outside the context.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)


# now we can start creating rag pipeline

#a function to combine the chunks
def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)

# the pipeline is built using Langchain expressive language
rag_chain = (
    {"context": retreiver | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# lets test the Chain (Command-Line Interface)
if __name__ == "__main__":
    print("\n--- EduLLM RAG Chain is Ready ---")
    print("All models loaded. The RAG chain is built.")
    print("Ask a question about your course materials (type 'exit' to quit):")
    
    while True:
        try:
            # Get user input from the command line
            query = input("> ")
            if query.lower() == 'exit':
                break
            if not query.strip():
                continue
                
            print("\nThinking...")
            
            # --- THIS IS THE "RETRIEVAL" STEP ---
            # When you call .invoke(query), you are "pulling the trigger"
            # on the entire chain. This is where the 'retriever'
            # is finally used to find chunks similar to your 'query'.
            answer = rag_chain.invoke(query)
            
            print("\n--- Answer ---")
            print(answer)
            print("--------------\n")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break

print("Exiting EduLLM...")