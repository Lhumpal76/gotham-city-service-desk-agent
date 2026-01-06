from sentence_transformers import SentenceTransformer
import sqlite3
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def main():
    print("Setting up FAISS index from database records...")

    # Connect to the database
    conn = sqlite3.connect('database/gotham_service_desk.db')
    cursor = conn.cursor()

    # Query tickets with non-null resolutions
    cursor.execute('''
        SELECT id, title, assigned_to, status, priority, resolution
        FROM tickets
        WHERE resolution IS NOT NULL
    ''')

    # Fetch results
    tickets = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    print(f"Retrieved {len(tickets)} tickets with non-null resolutions")

    # Close database connection
    conn.close()

    # Convert to list of dictionaries for easier processing
    ticket_dicts = []
    for ticket in tickets:
        ticket_dict = {column_names[i]: ticket[i] for i in range(len(column_names))}
        ticket_dicts.append(ticket_dict)

    # Use HuggingFaceEmbeddings to wrap the SentenceTransformer model
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Prepare texts and metadata for FAISS
    texts = []
    metadatas = []

    for ticket in ticket_dicts:
        # Text to embed - combine title and resolution
        text = f"Title: {ticket['title']} Resolution: {ticket['resolution']}"
        texts.append(text)

        # Metadata - keep all ticket information for retrieval
        metadata = {
            "id": ticket["id"],
            "title": ticket["title"],
            "assigned_to": ticket["assigned_to"],
            "status": ticket["status"],
            "priority": ticket["priority"],
            "resolution": ticket["resolution"]
        }
        metadatas.append(metadata)

    # Create FAISS vector store with texts, embeddings, and metadata
    print("Creating FAISS index...")
    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings_model,
        metadatas=metadatas
    )

    # Save the FAISS index to disk
    vectorstore.save_local("database/faiss_index")

    print(f"Number of embeddings: {len(texts)}")
    print(f"FAISS index saved to database/faiss_index")

if __name__ == "__main__":
    main()
