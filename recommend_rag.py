import os
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.docstore.document import Document
from functools import lru_cache

def hybrid_rerank(retrieved_docs_with_scores: list, rating_boost: float, dnf_penalty: float) -> list[Document]:
    reranked_results = []
    
    for doc, score in retrieved_docs_with_scores:
        meta = doc.metadata
        adjustment = 0.0
        
        if meta.get('rating', 0) >= 4:
            adjustment -= rating_boost
        
        shelf = meta.get('shelf', '').lower()
        if 'dnf' in shelf or 'did-not-finish' in shelf:
            adjustment += dnf_penalty
            
        new_score = score + adjustment
        
        doc.metadata['rerank_score'] = float(f"{new_score:.4f}")
        doc.metadata['original_score'] = float(f"{score:.4f}")
        doc.metadata['adjustment'] = float(f"{adjustment:+.2f}")
        
        reranked_results.append((doc, new_score))

    reranked_results.sort(key=lambda x: x[1], reverse=False)
    
    return [doc for doc, _ in reranked_results]

@lru_cache(maxsize=1) 
def get_vectorstore(persist_dir: str, embed_model: str):
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"Vector store not found at '{persist_dir}'. Run ingest.py first.")
        
    embeddings = OllamaEmbeddings(model=embed_model)
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectorstore

def get_recommendation(
    blurb: str, 
    persist_dir: str, 
    chat_model: str, 
    embed_model: str, 
    k: int,
    rating_boost: float = 0.3,
    dnf_penalty: float = 0.4
):
    vectorstore = get_vectorstore(persist_dir, embed_model)
    initial_candidates_with_scores = vectorstore.similarity_search_with_score(query=blurb, k=20)
    
    if not initial_candidates_with_scores:
        return {"explanation": "Keine relevanten Bücher in der Lesehistorie gefunden.", "contexts": []}

    pinned_dnf_doc = None
    remaining_candidates = list(initial_candidates_with_scores) # Kopie erstellen

    for i, (doc, score) in enumerate(initial_candidates_with_scores[:5]):
        shelf = doc.metadata.get("shelf", "").lower()
        if 'dnf' in shelf or 'did-not-finish' in shelf:
            pinned_dnf_doc = doc
            pinned_dnf_doc.metadata['is_pinned_match'] = True
            
            remaining_candidates.pop(i) 
            break 

    final_context_docs = []
    if pinned_dnf_doc:

        reranked_others = hybrid_rerank(
            remaining_candidates, 
            rating_boost=rating_boost, 
            dnf_penalty=dnf_penalty
        )
        final_context_docs = [pinned_dnf_doc] + reranked_others[:k-1]
    else:
        reranked_docs = hybrid_rerank(
            initial_candidates_with_scores, 
            rating_boost=rating_boost, 
            dnf_penalty=dnf_penalty
        )
        final_context_docs = reranked_docs[:k]

    if not final_context_docs:
        return {"explanation": "Keine relevanten Bücher in der Lesehistorie gefunden.", "contexts": []}

    context_string = "\n---\n".join([doc.page_content for doc in final_context_docs])
    
    template = """
    You are a brutally honest personalized book analysis assistant. Your task is to predict if a user will like a new book based on their reading history.
    Your analysis must be direct and based ONLY on the evidence provided in the context. Answer in German.

    **CRITICAL ANALYSIS RULES:**
    1.  **THE RATING IS TRUTH:** The user's star rating (`My Rating`) and shelf status (`Shelf Status`) are the ultimate source of truth. A 4 or 5-star rating is ALWAYS a positive signal, regardless of any critical comments in the review. A 'DNF' (Did Not Finish) status is the STRONGEST POSSIBLE NEGATIVE signal.
    2.  **DNF IS LAW:** If the context contains a DNF book that is similar to the new book (especially if it is marked as a 'pinned match'), you MUST predict the user will NOT like the new book. Your primary reason MUST be the existence of this DNF book.
    3.  **REASONING:** Base your conclusion entirely on the user's explicit ratings and shelf status. Compare themes and genres, but always tie it back to the user's final opinion (rating/DNF).
    4.  **VERDICT:** Conclude with a clear, unambiguous verdict: "Wahrscheinlich wirst du dieses Buch mögen." or "Wahrscheinlich wirst du dieses Buch NICHT mögen."

    **NEW BOOK BLURB:** {query}

    ---
    **CONTEXT (Similar books from the user's history):**
    {context}
    ---

    Based on your critical analysis of the context, provide a concise, personalized prediction.
    """
    prompt = PromptTemplate.from_template(template)
    
    llm = OllamaLLM(model=chat_model)
    
    rag_chain = (
        {"context": RunnableLambda(lambda x: context_string), 
         "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = rag_chain.invoke(blurb)
    
    return {
        "explanation": response, 
        "contexts": final_context_docs
    }