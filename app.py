import gradio as gr
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

# Load models and data
model_name = "sentence-transformers/all-mpnet-base-v2"
model = SentenceTransformer(model_name)

index = faiss.read_index("faiss/faiss_index.index")
with open("faiss/chunks_mapping.pkl", "rb") as f:
    token_split_texts = pickle.load(f)

# API Key (über Hugging Face secrets setzen)
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Retrieval
def retrieve_improved(query, top_k=5, search_k=100):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, search_k)
    candidate_chunks = [token_split_texts[i] for i in indices[0]]
    candidate_embeddings = np.array([model.encode(candidate_chunks, convert_to_numpy=True)][0])
    similarities = cosine_similarity(query_embedding, candidate_embeddings)[0]
    reranked_indices = np.argsort(similarities)[::-1][:top_k]
    final_chunks = [candidate_chunks[i] for i in reranked_indices]
    return final_chunks

# Simple Expansion
def simple_expansion(query):
    expansions = {
        "first proposal": ["Hunsford"],
        "second ball": ["Netherfield Ball", "Bingley", "Darcy", "assembly"],
    }
    for key, terms in expansions.items():
        if key in query:
            query += " " + " ".join(terms)
    return query

# Prompt builder
def build_prompt(context_chunks, user_query):
    context_block = "\n\n".join(context_chunks)
    return f"""You are a literary assistant specialized in Pride and Prejudice. Use only the context to answer.

Context:
{context_block}

Question: {user_query}
Answer:"""

# Full pipeline
def rag_pipeline(user_query):
    expanded_query = simple_expansion(user_query)
    retrieved_chunks = retrieve_improved(expanded_query)
    prompt = build_prompt(retrieved_chunks, user_query)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": "You are a literary assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Gradio Interface
gr.Interface(fn=rag_pipeline, inputs="text", outputs="text", title="Pride & Prejudice RAG").launch()
