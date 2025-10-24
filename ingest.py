import utils.prep as ingest
from langchain_ollama import OllamaEmbeddings
# [FIX 1] Import Chroma from langchain_community to fix the deprecation warning
from langchain_community.vectorstores import Chroma
import os

def main():
    GOODREADS_CSV_PATH = "utils/goodreads_with_blurbs.csv"
    PERSIST_DIRECTORY = "my_book_vectorstore"
    EMBEDDING_MODEL = "nomic-embed-text"

    df = ingest.load_and_prep_data(GOODREADS_CSV_PATH)
    if df is None or df.empty:
        print("No data to process. Exiting.")
        return

    documents = ingest.create_book_documents(df)
    if not documents:
        print("No documents were created. Exiting.")
        return

    print(f"Initializing embedding model: {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    print(f"Creating vector store in directory: {PERSIST_DIRECTORY}...")
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
    

    # --- [FIX 2] Batch the Ingestion Process ---
    # The '500 EOF' error means the Ollama server is crashing because
    # we're sending all 124 documents at once.
    # We will add them in small batches instead.
    
    batch_size = 1  # A safe, small batch size for local models
    total_docs = len(documents)
    
    if total_docs == 0:
        print("No documents to add. Exiting.")
        return
        
    # Calculate the total number of batches
    total_batches = (total_docs + batch_size - 1) // batch_size
    print(f"Adding {total_docs} documents in {total_batches} batches of {batch_size}...")

    # Add the first batch using .from_documents() to create the store
    first_batch = documents[0:batch_size]
    print(f"  ... adding batch 1/{total_batches}")
    vectorstore = Chroma.from_documents(
        documents=first_batch,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Add all remaining documents in batches using .add_documents()
    if total_batches > 1:
        for i in range(batch_size, total_docs, batch_size):
            batch = documents[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            print(f"  ... adding batch {batch_num}/{total_batches}")
            vectorstore.add_documents(documents=batch)
    
    # --- [End of Fix] ---
    
    print("\n--- Success! ---")
    print(f"Vector store has been created and saved at '{PERSIST_DIRECTORY}'")
    print(f"You can now use this vector store to query your reading history.")


if __name__ == "__main__":
    main()
