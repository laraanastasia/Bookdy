def main():
    import utils.prep as ingest
    from langchain_ollama import OllamaEmbeddings
    from langchain.vectorstores import Chroma
    import os
    GOODREADS_CSV_PATH = "data/goodreads_library_export.csv"
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
    

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("\n--- Success! ---")
    print(f"Vector store has been created and saved at '{PERSIST_DIRECTORY}'")
    print(f"You can now use this vector store to query your reading history.")


if __name__ == "__main__":
    main()