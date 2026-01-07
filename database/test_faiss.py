from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def test_query(vectorstore, query, k=3):
    """Test a specific query against the FAISS index."""
    print(f"\nTesting search with query: '{query}'")

    # Perform similarity search
    results = vectorstore.similarity_search(query, k=k)

    # Print results
    print(f"\nTop {k} most similar tickets:")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Ticket ID: {doc.metadata['id']}")
        print(f"Title: {doc.metadata['title']}")
        print(f"Resolution: {doc.metadata['resolution']}")
        print("-" * 50)

    return results

def main():
    """Test loading the FAISS index and performing similarity searches."""
    print("Loading FAISS index from database/faiss_index...")

    # Initialize the same embedding model with caching
    embeddings_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        cache_folder="database/models"  # This will use the cached model
    )

    # Load the FAISS index from disk
    # Set allow_dangerous_deserialization=True since we're loading our own file
    # Use relative path "./faiss_index" when running from database directory
    vectorstore = FAISS.load_local("database/faiss_index", embeddings_model, allow_dangerous_deserialization=True)

    print(f"FAISS index loaded successfully with {vectorstore.index.ntotal} vectors")

    # Test with multiple queries
    test_queries = [
        "Break-in at Wayne Tower",
        "Arson incident in Gotham",
        "Smuggling operation",
        "Bank robbery in progress"
    ]

    for query in test_queries:
        test_query(vectorstore, query)

if __name__ == "__main__":
    main()