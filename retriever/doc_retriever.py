# # retriever/doc_retriever.py
# import sys
# import os

# # Add the parent directory (RAG) to Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from config.settings import GEMINI_API_KEY

# import os
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# #from config.settings import GEMINI_API_KEY

# # Constants
# POLICY_FOLDER = "data/policies"
# CHROMA_DB_DIR = "retriever/chroma_db"

# # Set up embedding model
# embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GEMINI_API_KEY)

# def load_and_split_documents():
#     docs = []
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

#     for file in os.listdir(POLICY_FOLDER):
#         if file.endswith(".txt"):
#             loader = TextLoader(os.path.join(POLICY_FOLDER, file), encoding="utf-8")
#             text_docs = loader.load()
#             split_docs = splitter.split_documents(text_docs)
#             docs.extend(split_docs)

#     return docs

# def get_vector_store():
#     if not os.path.exists(CHROMA_DB_DIR):
#         os.makedirs(CHROMA_DB_DIR)

#     docs = load_and_split_documents()
#     vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=CHROMA_DB_DIR)
#     # vectordb.persist()
#     return vectordb

# def search_similar_documents(query, k=4):
#     vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding)
#     results = vectordb.similarity_search(query, k=k)
#     return [doc.page_content for doc in results]

# # Optional CLI test
# if __name__ == "__main__":
#     store = get_vector_store()
#     print("✅ Vector store created successfully!")

# retriever/doc_retriever.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import GEMINI_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
POLICY_FOLDER = "data/policies"
CHROMA_DB_DIR = "retriever/chroma_db"

# ✅ Embedding model
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

# ✅ Load and split only policy files
def load_and_split_documents():
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    for file in os.listdir(POLICY_FOLDER):
        if file.endswith(".txt") and "policy" in file.lower():  # load only policy files
            file_path = os.path.join(POLICY_FOLDER, file)
            loader = TextLoader(file_path, encoding="utf-8")
            text_docs = loader.load()
            split_docs = splitter.split_documents(text_docs)
            docs.extend(split_docs)

    return docs

# ✅ Create vector store & persist
def get_vector_store():
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    docs = load_and_split_documents()

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=CHROMA_DB_DIR
    )
    vectordb.persist()  # ✅ persist the DB
    return vectordb

# ✅ Search similar documents
# def search_similar_documents(query, k=4):
#     vectordb = Chroma(
#         persist_directory=CHROMA_DB_DIR,
#         embedding_function=embedding
#     )
#     results = vectordb.similarity_search(query, k=k)

#     # 🧪 Debug print
#     print(f"\n[DEBUG] Retrieved {len(results)} document chunks for query: '{query}'\n")
#     for i, doc in enumerate(results):
#         print(f"[{i+1}] {doc.page_content[:300]}...\n")  # Preview first 300 chars

#     return [doc.page_content for doc in results]
def search_similar_documents(query, k=4):
    vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding)
    results = vectordb.similarity_search(query, k=k)
    print(f"\n🔍 RAG Search Results for: {query}")
    for r in results:
        print("•", r.page_content[:200])
    return [doc.page_content for doc in results]


# ✅ CLI Test
if __name__ == "__main__":
    store = get_vector_store()
    print("✅ Vector store created and persisted successfully!")
