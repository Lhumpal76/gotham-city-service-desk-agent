import sqlite3
from pydantic_ai import RunContext
from agent.deps import AgentDeps
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

"""
Tool definitions for the Gotham Service Desk Agent.

All tools receive a RunContext[AgentDeps] parameter when called by the agent.
The agent object is passed in during registration in init_agent.py.
"""

def fetch_ticket(ctx: RunContext[AgentDeps], ticket_id: int):
    """
    Fetch a ticket by its ID from the SQLite database.

    Args:
        ctx (RunContext[AgentDeps]): Runtime context containing dependencies.
        ticket_id (int): ID of the ticket to retrieve.

    Returns:
        dict | None: A dictionary representing the ticket if found; None otherwise.
    """
    print(f"[FETCH TICKET TOOL CALLED] fetch_ticket with ticket_id={ticket_id}")

    db_path = ctx.deps.db_location

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    ticket_dict = dict(row)
    print(f"[FETCH TICKET RESULT] {ticket_dict}")
    return ticket_dict


def find_similar_tickets(ctx: RunContext[AgentDeps], query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Find tickets similar to the query using vector similarity search (RAG).

    Use this tool to search for tickets that are semantically similar to a given query.
    This is useful for finding related issues, past resolutions, or tickets with similar problems.

    Args:
        ctx (RunContext[AgentDeps]): Runtime context containing dependencies.
        query (str): The search query describing the ticket or issue to find similar tickets for.
        top_k (int): Maximum number of similar tickets to return. Defaults to 3.

    Returns:
        List[Dict[str, Any]]: List of similar ticket metadata with similarity scores.
    """
    print(f"[RAG TOOL CALLED] find_similar_tickets with query='{query}', top_k={top_k}")

    try:
        # Load the FAISS vectorstore
        embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            cache_folder="database/models"
        )

        vectorstore = FAISS.load_local(
            "database/faiss_index",
            embeddings_model,
            allow_dangerous_deserialization=True
        )

        # Perform similarity search with scores
        results = vectorstore.similarity_search_with_score(query, k=top_k)

        # Format results
        similar_tickets = []
        for doc, score in results:
            # Convert score to similarity (FAISS returns L2 distance, lower is better)
            similarity = 1.0 / (1.0 + score)

            # Add similarity score to metadata
            metadata = doc.metadata.copy()
            metadata["similarity"] = round(similarity, 3)
            similar_tickets.append(metadata)

        return similar_tickets
    except Exception as e:
        return [{"error": f"Error finding similar tickets: {str(e)}"}]


# Add more tools here as needed
