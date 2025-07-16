# from langchain_google_genai import ChatGoogleGenerativeAI
# from config.settings import GEMINI_API_KEY
# from retriever.doc_retriever import search_similar_documents
# import google.generativeai as genai

# # Configure native Gemini 1.5 Flash
# genai.configure(api_key=GEMINI_API_KEY)
# native_model = genai.GenerativeModel("models/gemini-1.5-flash")

# # LangChain-compatible model (used only if needed)
# llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

# # Final response logic
# def chat_with_agent(prompt):
#     docs = search_similar_documents(prompt)
    
#     if docs:
#         context = "\n".join(docs)
#         prompt_with_context = f"""You're a helpful assistant at TechProjects. Use the below documents to answer if relevant:

# {context}

# User Question: {prompt}

# If the answer isn't in the docs, respond naturally using your own knowledge.
# """
#         response = native_model.generate_content(prompt_with_context)
#         return response.text.strip()

#     # Fallback to general model
#     response = native_model.generate_content(prompt)
#     return response.text.strip()

# ✅ agent/gen_agent.py

from config.settings import GEMINI_API_KEY
from retriever.doc_retriever import search_similar_documents
import google.generativeai as genai

# ✅ Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ Smart dynamic answer (doc + general knowledge)
def smart_answer(prompt):
    docs = search_similar_documents(prompt)
    context = "\n".join(docs) if docs else ""

    # 🔍 Ask Gemini whether context is useful
    relevance_prompt = f"""
You are an assistant deciding if the following content is relevant to the question.

Question: "{prompt}"

Context:
\"\"\"
{context}
\"\"\"

Is the context directly useful for answering the question? Reply only "yes" or "no".
"""
    relevance_response = model.generate_content(relevance_prompt)
    relevance = relevance_response.text.strip().lower()

    # 📌 Decide answer mode
    if relevance.startswith("yes") and context:
        answer_prompt = f"""
You are TechProjects' assistant.

Use the internal policy documents to answer this question.

Documents:
\"\"\"
{context}
\"\"\"

Question: {prompt}

Answer based strictly on the documents.
"""
    else:
        answer_prompt = f"""
Answer the following using your general knowledge.

Question: {prompt}

Be helpful, informative, and direct.
"""

    # ✅ Final Answer
    final_response = model.generate_content(answer_prompt)
    return final_response.text.strip()

# ✅ Main callable function for app.py
def chat_with_agent(prompt):
    return smart_answer(prompt)
